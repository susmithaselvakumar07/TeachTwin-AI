def find_relevant_context(materials, question):

    question = question.lower()

    keywords = question.split()

    best_context = ""

    for text in materials:

        lower_text = text.lower()

        score = 0

        for word in keywords:
            if word in lower_text:
                score += 1

        if score > 0:
            best_context += text + "\n\n"

    return best_context
