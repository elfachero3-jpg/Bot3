# --- Lesson Analysis and AI Generation Functions ---------------------------
from google.genai import types
import prompts

# --- Lesson Analysis -------------------------------------------------------
def analyze_lesson_context(transcription: str, client, config) -> str:
    """
    Analyze the lesson to identify type, grade level, and focus
    
    Args:
        transcription: Teacher audio transcription
        client: Gemini API client
        config: Generation configuration
    
    Returns:
        Analysis summary as string
    """
    try:
        prompt = f"""Analyze this music lesson transcription and identify:
1. Lesson type (e.g., general music, instrumental, vocal, theory)
2. Approximate grade level
3. Main teaching focus and objectives
4. Key pedagogical approaches observed

Transcription:
{transcription}

Provide a concise analysis in 2-3 sentences."""
        
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[types.Content(parts=[types.Part(text=prompt)])],
            config=config,
        )
        return response.text
    except Exception as e:
        return f"Lesson analysis could not be completed: {str(e)}"


# --- Best Practices Research -----------------------------------------------
def research_best_practices(lesson_analysis: str, client, config) -> str:
    """
    Research relevant best practices based on lesson context
    
    Args:
        lesson_analysis: Output from analyze_lesson_context
        client: Gemini API client
        config: Generation configuration (with search tool)
    
    Returns:
        Research summary as string
    """
    try:
        prompt = f"""Based on this lesson analysis, research and summarize current best practices in music education for this context:

{lesson_analysis}

Focus on:
1. Pedagogical strategies for this lesson type and grade level
2. Current research on effective teaching methods
3. Recommended approaches from music education literature

Provide a concise summary with specific, actionable insights."""
        
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[types.Content(parts=[types.Part(text=prompt)])],
            config=config,
        )
        return response.text
    except Exception as e:
        return f"Best practices research completed with general music education principles. (Note: {str(e)})"


# --- Report Generation Prompt Call ----------------------------------------
def generate_observation_report(
    lesson_analysis: str,
    best_practices: str,
    aligned_teacher: str,
    aligned_observer: str,
    evaluation_criteria: str,
    report_sections: list,
    report_length: str,
    client,
    config
) -> str:
    """
    Generate comprehensive observation report
    
    Args:
        lesson_analysis: Lesson context analysis
        best_practices: Research summary
        aligned_teacher: Aligned teacher transcription
        aligned_observer: Aligned observer notes
        evaluation_criteria: Optional rubric/criteria
        report_sections: Sections to include
        report_length: Brief/Standard/Comprehensive
        client, config: Gemini client and generation config
    
    Returns:
        The generated report text
    """
    try:
        prompt = prompts.get_report_generation_prompt(
            lesson_analysis,
            best_practices,
            aligned_teacher,
            aligned_observer,
            evaluation_criteria,
            report_sections,
            report_length
        )
        
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[types.Content(parts=[types.Part(text=prompt)])],
            config=config,
        )
        return response.text
    except Exception as e:
        raise Exception(f"Report generation failed: {str(e)}")


# --- Solo Teaching Feedback Conversation ----------------------------------
def solo_feedback_conversation(
    transcription: str,
    chat_history: list,
    user_message: str,
    client,
    config
) -> str:
    """
    Generate reflective coaching response for solo teaching mode
    
    Args:
        transcription: Teacher's classroom audio transcription
        chat_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
        user_message: Current user message (empty string triggers first message)
        client: Gemini API client
        config: Generation configuration with solo coaching instructions
    
    Returns:
        AI assistant response as string
    """
    try:
        # Build conversation context
        conversation_parts = []
        
        # FIRST MESSAGE: Generate initial feedback automatically
        if len(chat_history) == 0:
            first_message_prompt = f"""CLASSROOM AUDIO TRANSCRIPTION:
{transcription}

This is the very first message. Follow the FirstMessageFormat instructions in your system prompt exactly:
1. Start with: "Thank you for sharing this teaching segment with me."
2. Identify 3 specific strengths with concrete examples from the transcription
3. Identify 2 specific areas for improvement with concrete examples
4. End with: "Do you have any questions about those items?"
5. Keep it to 3-4 sentences maximum
6. Use timestamps when helpful to ground examples

Generate your initial feedback now."""
            
            conversation_parts.append(types.Part(text=first_message_prompt))
        
        # SUBSEQUENT MESSAGES: Normal conversation flow
        else:
            # Add transcription context reference
            conversation_parts.append(types.Part(text=f"""CLASSROOM AUDIO TRANSCRIPTION REFERENCE:
{transcription}

Continue the reflective coaching conversation based on the chat history below."""))
            
            # Add chat history
            for msg in chat_history:
                role = "user" if msg["role"] == "user" else "model"
                conversation_parts.append(types.Part(text=msg["content"]))
            
            # Add current user message
            conversation_parts.append(types.Part(text=user_message))
        
        # Generate response
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=[types.Content(parts=conversation_parts)],
            config=config,
        )
        
        return response.text
        
    except Exception as e:
        raise Exception(f"Solo feedback conversation failed: {str(e)}")
