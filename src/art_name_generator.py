import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def new_example(c1: str, c2: str, name: str):
    return f"[{c1}, {c2}]: {name} #"


def generate_name_with_retry(
    start_color: str, end_color: str, name_set: set = None, max_retry: int = 3
):
    for _ in range(max_retry):
        name = generate_name(start_color, end_color, name_set=name_set)
        if name is not None:
            return name
    
    raise Exception(f"Unable to find name after {max_retry} retries")


def generate_name(start_color: str, end_color: str, name_set: set = None):

    examples = [
        new_example("Black", "Red Ochre", "Waiting for death"),
        new_example("Ocean Blue", "Emerald", "Outworn patterns of thought"),
        new_example("Gold", "Picton Blue", "Golden ocean"),
        new_example("Malachite", "Spring Green", "Verdant Jungle"),
        new_example("Purple", "Deep Koamaru", "Void vector"),
        new_example("Clementine", "Red", "Flamingo sunset"),
        new_example("Zest", "Bright Turquoise", "Lullaby"),
    ]

    prompt = (
        f"Poetic titles of abstract artwork based on color: \n\n"
        + "\n".join(examples)
        + f"\n[{start_color}, {end_color}]:"
    )

    response = openai.Completion.create(
        engine="curie",
        prompt=prompt,
        max_tokens=24,
        stop=["#"],
        temperature=0.85,
        presence_penalty=0.7,
        frequency_penalty=0.7,
        n=3,
    )

    titles = [r["text"].strip("\n").strip(" ") for r in response["choices"]]
    titles.sort(key=lambda x: len(x))

    print(f"Possible Names: {titles}")

    if name_set is not None:
        # Avoid naming collisions.
        for title in titles:
            if title not in name_set:
                name_set.add(title)
                return title
        return None
    else:
        art_title = titles[0]
        return art_title
