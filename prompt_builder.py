def build_prompt(search):

    company = search["company"]

    employment_type = search["employment_type"]

    open_to_work = search["open_to_work"]

    if employment_type == "current":

        prompt = (
            f"Current employees of {company}"
        )

    else:

        prompt = (
            f"Past employees of {company}"
        )

    if open_to_work:

        prompt += " who are open to work"

    return prompt