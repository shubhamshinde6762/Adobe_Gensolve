import React from "react";
import Lottie from "react-lottie";
import anim5 from "./lottie/anim3.json";
import Canvas from "./Canvas";

const anim5o = {
  loop: true,
  autoplay: true,
  animationData: anim5,
  rendererSettings: {
    preserveAspectRatio: "xMidYMid slice",
  },
};

const Home = () => {
  return (
    <div className="bg-stone-900 flex justify-center items-center w-full h-screen overflow-hidden">
      <div className="w-[50vh] right-0 -bottom-0 z-50 absolute flex justify-center items-center ">
        {/* <div className=" min-w-[240px]">
          <Lottie options={anim5o} />
        </div> */}
      </div>

      <Canvas />
    </div>
  );
};

export default Home;
