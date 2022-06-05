def test_safe_mint(poofpoof, owner, token_receiver, metadata_cid):
    receipt = poofpoof.safeMint(token_receiver, "0.json", sender=owner)
    assert receipt

    actual_token_uri = poofpoof.tokenURI(0)
    expected_token_uri = f"{metadata_cid}0.json"
    assert actual_token_uri == expected_token_uri
