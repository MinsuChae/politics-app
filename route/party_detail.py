from flask import render_template, redirect, url_for
from data.data_loader import parties_by_slug as get_parties_by_slug

def party_detail(party_slug):
    current_parties_by_slug = get_parties_by_slug()
    party = current_parties_by_slug.get(party_slug)
    if not party:
        return "Party not found.", 404

    if len(party["candidates"]) == 1:
        return redirect(url_for(
            'candidate_detail',
            party_slug=party_slug,
            candidate_index=0
        ))

    return render_template('party_detail.html', party=party)

