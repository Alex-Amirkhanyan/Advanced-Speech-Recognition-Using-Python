import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unrecognizable
        response["error"] = "Unable to recognize speech"

    return response

if __name__ == "__main__":
    # set up the recognizer and microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # show instructions to the user
    print("Say something!")

    # recognize speech and check the response
    response = recognize_speech_from_mic(recognizer, microphone)
    if response["transcription"]:
        # show the user the transcription
        print("You said: {}".format(response["transcription"]))
    if not response["success"]:
        print("I'm sorry, I didn't catch that. What did you say?\n")
    if response["error"]:
        print("ERROR: {}".format(response["error"]))
