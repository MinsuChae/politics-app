from flask import render_template
from data.data_loader import parties_by_slug as get_parties_by_slug

def candidate_detail(party_slug, candidate_index):
    current_parties_by_slug = get_parties_by_slug()

    party = current_parties_by_slug.get(party_slug)
    if not party or candidate_index < 0 or candidate_index >= len(party["candidates"]):
        return "Candidate not found.", 404

    candidate = party["candidates"][candidate_index]
    return render_template(
        'candidate_detail.html',
        party=party,
        candidate=candidate,
        party_slug=party_slug,
        candidate_index=candidate_index
    )