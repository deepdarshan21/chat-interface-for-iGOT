import "./App.css";
import { useEffect, useRef, useState } from "react";
import { DeepChat } from "deep-chat-react";
import Fab from "@mui/material/Fab";
import SmartToyIcon from "@mui/icons-material/SmartToy";

function App() {
  const [showChat, setShowChat] = useState(false);
  const initialMessages = [
    // { role: "user", text: "Hey, how are you today?" },
    { role: "ai", text: "Hey! How can I help you today?" },
    {
      role: "ai",
      html: "<p> Ask me anything related to - <br></p><ul><li>Give me a course related to python</li><li>Provide the summary of the course 'Python Fundamentals'</li><li>Test my knowledge</li><li>Ask anything</li></ul>",
    },
  ];
  const chatElementRef = useRef(null);

  useEffect(() => {
    if (chatElementRef.current) {
      // chatElementRef.current.messageStyles = {
      //   html: {
      //     shared: {
      //       bubble: {
      //         backgroundColor: "unset",
      //         padding: "0px",
      //         width: "100%",
      //         textAlign: "right",
      //       },
      //     },
      //   },
      // };

      chatElementRef.current.submitButtonStyles = {
        disabled: { container: { default: { opacity: 0, cursor: "auto" } } },
      };

      chatElementRef.current.onNewMessage = ({ message, isInitial }) => {
        
        const allMessages = chatElementRef.current.getMessages();
        if (
          !isInitial &&
          message.role === "ai" &&
          message.text !== "Thanks recorded!" &&
          message.html.search(/<button/g) === -1
        ) {
          console.log("in ref : ", isInitial, message);

          chatElementRef.current._addMessage({
            text: "Was the response satisfactory?",
            role: "ai",
          });
          chatElementRef.current._addMessage({
            role: "user",
            html: `
            <div class="deep-chat-temporary-message">
              <button class="deep-chat-button deep-chat-suggestion-button" style="border: 1px solid green">Yes</button>
              <button class="deep-chat-button deep-chat-suggestion-button" style="border: 1px solid #d80000">No</button>
            </div>`,
          });
        }

        if (
          !isInitial &&
          allMessages.length !== 0 &&
          allMessages[allMessages.length - 2].role === "ai" &&
          allMessages[allMessages.length - 2].html.search(/<button/g) !== -1 &&
          allMessages[allMessages.length - 2].html.match(/<button/g).length >= 4
        ) {
          console.log("ye tha resopnses - ", message.text);
        }
      };

      chatElementRef.current.responseInterceptor = (a) => {
        return a[0];
      };
    }
  }, []);
  return (
    <div className="App" style={{ position: "relative", height: "100vh" }}>
      <DeepChat
        ref={chatElementRef}
        style={{
          visibility: showChat ? "visible" : "hidden",
          position: "absolute",
          top: "calc(50% - 120px)", // Adjust this value based on the desired spacing and size of your DeepChat component
          // left: 0,
          right: 16,
          bottom: 0,
          borderRadius: "10px",
          zIndex: 1, // Ensure it's above other content
        }}
        request={{
          url: "http://127.0.0.1:5000/api/chat",
          method: "POST",
        }}
        // textToSpeech="true"
        speechToText={{
          webSpeech: true,
          translations: { hello: "goodbye", Hello: "Goodbye" },
          commands: { resume: "resume", settings: { commandMode: "hello" } },
          button: { position: "outside-left" },
        }}
        textInput={{ placeholder: { text: "Welcome to the demo!" } }}
        initialMessages={initialMessages}
      />

      <Fab
        color="primary"
        aria-label="add"
        onClick={() => setShowChat(!showChat)}
        style={{
          position: "absolute",
          bottom: 16, // Adjust the distance from the bottom as needed
          right: 16, // Adjust the distance from the right as needed
        }}
      >
        <SmartToyIcon />
      </Fab>
    </div>
  );
}

export default App;
