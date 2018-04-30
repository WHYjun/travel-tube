import React, { Component } from "react";
import { Header, Button } from "semantic-ui-react";

class Home extends Component {

  async componentDidMount() {}

  // user pressed login button
  async loginPressed() {
    console.log("login pressed");
    window.open("http://127.0.0.1:5000/login","_self");
  }

  loginButton = () => {
    return <Button onClick={() => this.loginPressed()}> Login </Button>;
  };
  render() {
    return (
      <div style={{ textAlign: "center" }}>
        <Header style={{ textAlign: "center" }} as="h1">
          {" "}
          TravelTube{" "}
        </Header>
        <div style={{ textAlign: "center" }}>{this.loginButton()}</div>
      </div>
    );
  }
}

export default Home;
