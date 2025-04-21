from flask import session, jsonify, request
import json
from transformers import AutoTokenizer, Gemma3ForCausalLM
import torch
from data.data_loader import parties_by_slug as get_parties_by_slug
from data.data_loader import get_all_candidates
import gc


model_id = "google/gemma-3-1b-it"
model = Gemma3ForCausalLM.from_pretrained(model_id, device_map="auto").eval()
tokenizer = AutoTokenizer.from_pretrained(model_id)

def __clear_memory__():
    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        torch.mps.empty_cache()

def __check_question_limit():
    if 'question_count' not in session:
        session['question_count'] = 0
    if session['question_count'] >= 3:
        return False
    session['question_count'] += 1
    return True

def __build_chat_messages(context_text, chat_history, question):
    system_prompt = {
        "role": "system",
        "content": "You are a helpful and kindly, useful assistant. If you provide a presidential candidate’s campaign pledges, I will respond clearly and appropriately in Korean to your questions. Because the pretraining data only goes up until 2024, information on the most recent presidential candidates is missing. You should provide information about the presidential candidates based on the list you received. Please answer the given question within 128 tokens."
    }
    messages = [system_prompt,
                {"role": "user", "content": context_text}, 
                {"role": "assistant", "content": "이해했습니다. 또한 다음답변부터는 한국어로 답변하겠습니다."}
                ]

    expected_roles = ["user", "assistant"]
    last_role = None
    for msg in chat_history:
        role = msg.get("role")
        content = msg.get("content", "").strip()
        if role not in expected_roles or not content or role == last_role:
            continue
        messages.append({"role": role, "content": content})
        last_role = role

    messages.append({"role": "user", "content": question})
    return messages

def __generate_answer(messages, max_new_tokens=128):
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    ).to(model.device)

    outputs = None
    try:
        with torch.inference_mode():
            outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
        raw = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return raw.split("model")[-1].strip()
    finally:
        del inputs, outputs


def ask_candidate(party_slug, candidate_index):
    if not __check_question_limit():
        return jsonify({"error": "잠시 후 다시 시도하세요."}), 429

    current_parties_by_slug = get_parties_by_slug()
    party = current_parties_by_slug.get(party_slug)
    if not party or candidate_index < 0 or candidate_index >= len(party["candidates"]):
        return jsonify({"error": "Invalid party or candidate"}), 404

    candidate = party["candidates"][candidate_index]
    data = request.get_json()
    chat_history = data.get("chat_history", [])
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    field_labels = {
        "name": "이름",
        "birth": "출생일",
        "current_position": "현직",
        "campaign_team": "선거캠프",
        "biography": "약력",
        "pledges": "공약",
        "controversies": "논란"
    }

    info = []
    for key in sorted(candidate):
        if key in field_labels:
            if key in ['pledges', 'controversies']:
                entries = []
                for item in candidate[key]:
                    lines = [f"{field_labels.get(k,k)} : {v}" for k, v in item.items()]
                    entries.append("\n".join(lines))
                joined_entries = "\n".join(entries)
                info.append(f"{field_labels[key]} : {joined_entries}")
            else:
                info.append(f"{field_labels[key]} : {candidate[key]}")
    context_text = "\n".join(info)

    try:
        messages = __build_chat_messages(context_text, chat_history, question)
        answer = __generate_answer(messages, max_new_tokens=384)
    except Exception as e:
        session['question_count'] -= 1
        del context_text
        __clear_memory__()
        return jsonify({"error": f"LLM error: {str(e)}"}), 500

    session['question_count'] -= 1
    del context_text
    __clear_memory__()
    return jsonify({"answer": answer})

def ask_all_candidates():
    if not __check_question_limit():
        return jsonify({"error": "잠시 후 다시 시도하세요."}), 429

    data = request.get_json()
    chat_history = data.get("chat_history", [])
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "질문을 입력해주세요."}), 400

    all_cands = get_all_candidates()
    field_labels = {
        "name": "이름",
        "party_name": "소속 정당",
        "birth": "출생일",
        "current_position": "현직",
        "campaign_team": "선거캠프",
        "biography": "약력",
        "pledges": "공약",
        "controversies": "논란"
    }

    lines = []
    for c in all_cands:
        lines.append(f"## {c['name']} ({c['party_name']})")
        for key in ["birth", "current_position", "campaign_team", "biography"]:
            if c.get(key):
                lines.append(f"{field_labels[key]} : {c[key]}")
        for p in c.get("pledges", []):
            lines.append(f"{field_labels['pledges']} - {p['title']}: {p.get('description','')}")
        for con in c.get("controversies", []):
            parts = [
                f"이슈: {con.get('issue','')}", f"내용: {con.get('details','')}",
                f"날짜: {con.get('date','')}", f"출처: {con.get('source','')}"
            ]
            lines.append(f"{field_labels['controversies']} - {' | '.join(parts)}")
        lines.append("\n==============\n")
    context_text = "\n".join(lines)

    try:
        messages = __build_chat_messages(context_text, chat_history, question)
        answer = __generate_answer(messages)
    except Exception as e:
        session['question_count'] -= 1
        del context_text
        __clear_memory__()
        return jsonify({"error": f"LLM error: {str(e)}"}), 500

    session['question_count'] -= 1
    del context_text
    __clear_memory__()
    return jsonify({"answer": answer})
