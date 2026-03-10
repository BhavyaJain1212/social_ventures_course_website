"""
Prompt Service — Generates rich design prompts from user inputs.

Converts structured form inputs into natural-language prompts
suitable for image generation models (DALL-E, Stable Diffusion, etc.)
and produces human-readable concept summaries.

---
LANGCHAIN INTEGRATION NOTE:
If LangChain is adopted later, this module can be refactored to use:
    - PromptTemplate for structured prompt creation
    - LLMChain for chaining recommendation + prompt generation
    - OutputParser for structured response formatting

Example (commented out):
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.llms import OpenAI

    prompt_template = PromptTemplate(
        input_variables=["craft_type", "product_type", "style",
                         "color_palette", "motif_direction", "target_audience"],
        template=(
            "Create a contemporary {craft_type} {product_type} design "
            "inspired by traditional {motif_direction} motifs, "
            "adapted for {target_audience}. "
            "Use colors: {color_palette}. "
            "Style: {style}. "
            "Keep motif density appropriate, preserve handloom authenticity, "
            "and make the overall aesthetic elegant, wearable, and modern."
        )
    )

    chain = LLMChain(llm=OpenAI(), prompt=prompt_template)
    result = chain.run(craft_type=..., product_type=..., ...)
---
"""


def build_design_prompt(craft_type, product_type, style="contemporary",
                        color_palette="", motif_direction="",
                        target_audience="general audience"):
    """
    Build a rich, natural-language design generation prompt.

    Args:
        craft_type (str): e.g., "Banarasi weaving"
        product_type (str): e.g., "stole"
        style (str): e.g., "pastel", "minimal", "festive"
        color_palette (str): e.g., "pastel rose, muted gold, ivory"
        motif_direction (str): e.g., "floral zari motifs"
        target_audience (str): e.g., "young urban professionals"

    Returns:
        str: A complete design prompt string.
    """
    # Normalize inputs
    craft = craft_type.strip() or "traditional Indian craft"
    product = product_type.strip() or "textile product"
    audience = target_audience.strip() or "modern consumers"
    colors = color_palette.strip() if color_palette else "harmonious earth tones and soft pastels"
    motifs = motif_direction.strip() if motif_direction else "traditional craft motifs"
    design_style = style.strip() if style else "contemporary"

    # Build the prompt with rich context
    prompt_parts = [
        f"Create a {design_style} {craft} {product} design",
        f"inspired by traditional {motifs},",
        f"adapted for {audience}.",
        f"Use a color palette of {colors}.",
        f"Keep motif density thoughtful and balanced,",
        f"preserve handcraft authenticity and artisanal character,",
        f"and make the overall aesthetic elegant, wearable, and modern.",
        f"The design should feel premium yet rooted in cultural tradition.",
    ]

    return " ".join(prompt_parts)


def generate_concept_summary(craft_type, product_type, style="contemporary",
                             color_palette="", motif_direction="",
                             target_audience="general audience"):
    """
    Generate a human-readable concept summary for the design idea.

    Returns:
        str: A short paragraph describing the design concept.
    """
    craft = craft_type.strip() or "traditional craft"
    product = product_type.strip() or "product"
    audience = target_audience.strip() or "modern consumers"
    colors = color_palette.strip() if color_palette else "harmonious tones"
    motifs = motif_direction.strip() if motif_direction else "traditional motifs"
    design_style = style.strip() if style else "contemporary"

    summary = (
        f"A {design_style} {product} concept rooted in {craft} traditions. "
        f"This design adapts {motifs} for {audience}, "
        f"using a palette of {colors}. "
        f"The concept balances authentic craftsmanship with modern market appeal, "
        f"making it suitable for today's design-conscious consumers while "
        f"honoring the artisan's traditional skills."
    )

    return summary


def generate_concept_title(craft_type, product_type, style="contemporary"):
    """
    Generate a concise, descriptive title for the design concept.

    Returns:
        str: A short title like "Contemporary Banarasi Stole Concept"
    """
    craft = craft_type.strip().title() if craft_type else "Artisan"
    product = product_type.strip().title() if product_type else "Design"
    design_style = style.strip().title() if style else "Contemporary"

    return f"{design_style} {craft} {product} Concept"
