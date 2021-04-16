import Widget from "rasa-webchat";

export default function CustomWidget() {
  return (
    <Widget
      initPayload={"Hi"}
      socketUrl={"http://localhost:5005"}
      socketPath={"/socket.io/"}
      customData={{ language: "de" }} // arbitrary custom data. Stay minimal as this will be added to the socket
      title={"Studienberatung"}
      storage="session"
    />
  );
}
