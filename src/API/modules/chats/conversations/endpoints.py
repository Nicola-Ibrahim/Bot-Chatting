from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, HTTPException, status
from shared.infra.utils.result import Result

from src.modules.chats.application.conversations.create_conversation import create_conversation_command

from .....modules.chats.infra.common.di import ChatAppDIContainer
from ..contract.conversation import ConversationResponseSchema, CreateConversationRequestSchema, MessageResponseSchema

router = APIRouter(
    prefix="/v1/conversation",
    tags=["conversation"],
    responses={404: {"description": "Not found"}},
)


@router.post("/conversations")
def create_conversation():
    command = create_conversation_command(user_id=1)
    return create_conversation_handler.execute(command)


@router.post("/conversations/{conversation_id}/messages")
def add_message(conversation_id: uuid.UUID, text: str):
    command = AddMessageCommand(conversation_id=conversation_id, text=text)
    return add_message_handler.execute(command)


@router.post("/conversations/{conversation_id}/messages/{message_id}/feedback")
def add_feedback(
    conversation_id: uuid.UUID, message_id: uuid.UUID, content_pos: int, rating: RatingType, comment: str
):
    command = AddFeedbackCommand(
        conversation_id=conversation_id, message_id=message_id, content_pos=content_pos, rating=rating, comment=comment
    )
    return add_feedback_handler.execute(command)


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: uuid.UUID):
    query = GetConversationByIdQuery(conversation_id=conversation_id)
    return get_conversation_handler.execute(query)


@router.get("", response_model=ConversationResponseSchema)
async def get(conversation_id: str):
    return


@router.post("", response_model=ConversationResponseSchema)
async def create(
    request: CreateConversationRequestSchema,
    conversation_service: ConversationApplicationService = Depends(Provide[ChatAppDIContainer.conversation_service]),
):
    conversation = request.map_to_conversation()

    result: Result = conversation_service.create(conversation=conversation)

    return result.match(
        # TODO: Apply on success {conversation.map_to_response()} or {conversation.as_dict()} for better serialization
        on_success=lambda conversation: ConversationResponseSchema(
            id=str(conversation.id),
            messages=[MessageResponseSchema(id=str(msg.id)) for msg in conversation.all_messages],
        ),
        on_failure=lambda error: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)),
    )


# @chat_page.route("/")
# def home():
#     """
#     Renders the home page of the application.

#     Returns:
#         str: Rendered HTML template for the home page.
#     """
#     return render_template("index.html", active_page="home")


# @chat_page.route("/dataset")
# def dataset():
#     """
#     Renders the dataset page, showing the structure of example tables.

#     Returns:
#         str: Rendered HTML template for the dataset page with table structure information.
#     """

#     structure = []
#     csv_folder = current_app.config["CSV_DATA_FOLDER"]
#     for filename in os.listdir(csv_folder):
#         if filename.endswith(".csv"):
#             # Get the full file path
#             file_path = os.path.join(csv_folder, filename)
#             # Read the CSV file into a DataFrame
#             df = pd.read_csv(file_path, nrows=0)  # Only read the header (first row)
#             # Extract the structure
#             table_structure = {
#                 "name": os.path.splitext(filename)[0],  # Use file name (without extension) as table name
#                 "columns": list(df.columns),  # Get column names
#             }
#             # Append to structure list
#             structure.append(table_structure)

#     # Pass both headers and data to the template
#     return render_template("dataset.html", active_page="dataset", structure=structure)


# @chat_page.route("/settings")
# def settings():
#     """
#     Renders the home page of the application.

#     Returns:
#         str: Rendered HTML template for the home page.
#     """
#     return render_template("settings.html", active_page="settings")


# @chat_page.route("/getAnswer")
# def generate_answer_from_prompt_api():
#     """
#     Generates an answer to a user's query using a pre-defined pipeline.

#     The answer is formatted and highlighted based on validated sentences.

#     Returns:
#         str: HTML-formatted and highlighted answer to the user's query.
#     """
#     try:
#         message = request.args.get("msg")

#         # Validate the input message using the valid_prompt function
#         if not valid_prompt(message):
#             # Return a more user-friendly error message
#             return jsonify({"error": "Please enter a valid question. The input cannot be empty or too short."}), 400

#         def generate():
#             result = [None, None, None]
#             error: Exception = None
#             streamer = FlaskStreamer(skip_prompt=True)

#             def run_model():
#                 global error
#                 try:
#                     result[0], result[1], result[2] = generate_answer_from_question(message, streamer)
#                 except Exception as e:
#                     logger.error("An Exception occured during generation: ", e)
#                     error = e

#             thread = threading.Thread(target=run_model, name="Generator")
#             thread.start()
#             while (not streamer.reached_end or not streamer.queue.empty()) and error == None:
#                 text = streamer.queue.get(block=True, timeout=7)
#                 yield json.dumps({"chunk": text, "answer": ""})
#             # Format and highlight the answer
#             thread.join()
#             if error:
#                 raise error
#             answer, validated_sentences, paths = result[0], result[1], result[2]
#             memory_manager.add_memory(message.strip(), answer.strip())
#             if answer != "" and validated_sentences != []:
#                 answer = text_helpers.highlight_words(text=answer, words_to_highlight=validated_sentences, paths=paths)
#                 answer = text_helpers.format_text_for_html(answer)
#             answer = answer.replace("\n", "<br>")
#             yield json.dumps({"chunk": "", "answer": answer})

#         return Response(generate(), mimetype="application/json")

#     except Exception as e:
#         logger.error("An Exception occured during processing the message: ", e)
#         return jsonify({"error": "Oops! Something went wrong. Please try again."}), 500


# def valid_prompt(message):
#     """
#     Validates the input message.

#     Args:
#         message (str): The user's input query.

#     Returns:
#         bool: True if the message is valid, False otherwise.
#     """
#     # Ensure the message is not empty or None
#     if not message or message.strip() == "":
#         return False

#     # Check if the message is too short or just a number
#     if len(message) < 3 or message.isdigit():
#         return False

#     # Add any additional validation criteria as needed
#     return True


# @chat_page.route("/image/<filename>")
# def get_image(filename):
#     """
#     Serves an image file from the 'image' directory based on the filename provided.

#     Args:
#         filename (str): The name of the image file to retrieve (without extension).

#     Returns:
#         Response: The image file in PNG format.
#     """
#     print(filename)
#     return send_file(f"image/{filename}.png", mimetype="image/png")


# # Route to get all feedbacks
# @chat_page.route("/feedbacks", methods=["GET"])
# def get_all_feedback():
#     feedbacks = file_feedback_manager.get_feedback()
#     return jsonify(feedbacks), 200


# # Route to get a specific feedback by ID
# @chat_page.route("/feedbacks/<int:feedback_id>", methods=["GET"])
# def get_feedback(feedback_id):
#     feedbacks = file_feedback_manager.get_feedback()
#     feedback = next((fb for fb in feedbacks if fb["id"] == feedback_id), None)
#     if feedback is None:
#         return abort(404, description=f"Feedback with ID {feedback_id} not found.")
#     return jsonify(feedback), 200


# # Route to add a new feedback (POST request)
# @chat_page.route("/feedbacks", methods=["POST"])
# def add_feedback():
#     if not request.json or not "feedback" in request.json:
#         return abort(400, description="Invalid input. 'comment' field is required.")

#     feedback_data = {"user": request.json.get("user", "Anonymous"), "feedback": request.json["feedback"]}

#     feedback_id = file_feedback_manager.add_feedback(feedback_data)
#     return jsonify({"message": "Feedback added successfully!", "feedback_id": feedback_id}), 201


# # Route to delete a feedback by ID
# @chat_page.route("/feedbacks/<int:feedback_id>", methods=["DELETE"])
# def delete_feedback(feedback_id):
#     feedbacks = file_feedback_manager.get_feedback()
#     feedback = next((fb for fb in feedbacks if fb["id"] == feedback_id), None)
#     if feedback is None:
#         return abort(404, description=f"Feedback with ID {feedback_id} not found.")

#     file_feedback_manager.delete_feedback(feedback_id)
#     return jsonify({"message": f"Feedback with ID {feedback_id} deleted successfully!"}), 200


# @chat_page.route("/getMemory", methods=["GET"])
# def get_all_memory():
#     memories = memory_manager.get_all_memory()
#     return jsonify(memories)


# @chat_page.route("/clearMemory", methods=["POST"])
# def clear_memory():
#     """Clears all stored memories."""
#     try:
#         memory_manager.clear_memory()
#         return jsonify({"message": "Memory cleared successfully"})
#     except Exception as e:
#         return jsonify({"error": "Failed to clear memory"}), 500


# @chat_page.route("/exportMemory", methods=["GET"])
# def export_memory():
#     """
#     Exports the chat memory as a .txt file for download.
#     """
#     try:
#         base_dir = os.path.abspath(os.path.dirname(__file__))

#         json_path = os.path.join(os.getcwd(), "chat_memory.json")
#         txt_path = os.path.join(os.getcwd(), "chat_memory.txt")

#         with open(json_path, "r") as f:
#             memory_data = json.load(f)

#         with open(txt_path, "w") as txt_file:
#             for mem in memory_data:
#                 txt_file.write(f"Q: {mem['question']}\nA: {mem['answer']}\n\n")

#         return send_file(txt_path, as_attachment=True)

#     except Exception as e:
#         print(f"Error exporting memory: {str(e)}")
#         return jsonify({"error": "Failed to export memory"}), 500
#         return jsonify({"error": "Failed to export memory"}), 500
