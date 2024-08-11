import { ReactSketchCanvas } from "react-sketch-canvas";
import { useEffect, useRef, useState } from "react";
import { BiEraser } from "react-icons/bi";
import { FaUndo, FaRedo, FaTrash, FaSync, FaUpload } from "react-icons/fa";
import LightModeIcon from "@mui/icons-material/LightMode";
import NightlightRoundIcon from "@mui/icons-material/NightlightRound";
import DrawIcon from "@mui/icons-material/Draw";
import { saveAs } from "file-saver";
import axios from "axios";
import Papa from "papaparse";
import Lottie from "react-lottie";
import anim5 from "./lottie/anim3.json";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import AutoFixHighIcon from "@mui/icons-material/AutoFixHigh";

const anim5o = {
  loop: true,
  autoplay: true,
  animationData: anim5,
  rendererSettings: {
    preserveAspectRatio: "xMidYMid slice",
  },
};

export default function App() {
  const canvasRef = useRef(null);
  const [eraseMode, setEraseMode] = useState(false);
  const [mode, setMode] = useState("white");
  const [autoCorrect, setAutoCorrect] = useState(0);
  const [isLoad, setLoading] = useState(false);

  const handleSaveClick = async () => {
    if (canvasRef.current) {
      await canvasRef.current
        .exportPaths()
        .then(async (paths) => {
          console.log("Exported Paths:", paths);

          if (paths && paths.length > 0) {
            const csvData = [];
            paths.forEach((pathObj, index) => {
              if (pathObj.paths && pathObj.paths.length > 0) {
                pathObj.paths.forEach((point) => {
                  csvData.push({
                    curveIndex: index,
                    static: "0.0000",
                    x: point.x.toFixed(3),
                    y: point.y.toFixed(3),
                  });
                });
              }
            });

            const csv = Papa.unparse(csvData, { header: true });
            const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
            const formData = new FormData();
            formData.append("file", blob, "drawing.csv");

            await axios
              .post("https://specific-fina-shubham6762-382e557a.koyeb.app//upload_csv", formData, {
                headers: {
                  "Content-Type": "multipart/form-data",
                },
              })
              .then((response) => {
                console.log("File uploaded successfully:", response.data);
                handleLoadClick(response.data);
              })
              .catch((error) => {
                console.error("Error uploading file:", error);
              });
          } else {
            console.error("No paths found to export.");
          }
        })
        .catch((error) => {
          console.error("Error exporting paths:", error);
        });
    }

    setLoading(false);
  };

  const handleLoadClick = (csvString) => {
    const lines = csvString.trim().split("\n");
    const paths = [];

    lines.forEach((line) => {
      const values = line.split(",");

      const curveIndex = parseInt(values[0]);
      const x = parseFloat(values[2]);
      const y = parseFloat(values[3]);

      if (!paths[curveIndex]) {
        paths[curveIndex] = {
          paths: [],
          drawMode: true,
          strokeWidth: 1,
          strokeColor: mode,
        };
      }

      // Add the point to the corresponding path
      paths[curveIndex].paths.push({ x, y });
    });

    console.log("Parsed Paths:", paths);

    // Load the paths into the ReactSketchCanvas
    if (canvasRef.current) {
      canvasRef.current.clearCanvas(); // Clear existing canvas before loading new paths
      canvasRef.current.loadPaths(paths); // Load the parsed paths into the canvas
    }
  };

  // const handleFileUpload = (event) => {
  //   const file = event.target.files[0];
  //   console.log(file)
  //   if (file) {
  //     const reader = new FileReader();

  //     reader.onload = (e) => {
  //       const csvString = e.target.result;
  //       console.log(csvString)
  //       handleLoadClick(csvString);
  //     };

  //     reader.readAsText(file);
  //   }
  // };

  // Trigger file upload dialog on clicking the upload icon
  // const handleUploadClick = () => {
  //   const input = document.createElement("input");
  //   input.type = "file";
  //   input.accept = ".csv";
  //   input.onchange = handleFileUpload;
  //   input.click();
  // };

  useEffect(() => {
    console.log("100");
    if (isLoad === true) handleSaveClick();
  }, [isLoad]);

  return (
    <div className="flex flex-col p-4 w-full h-full text-white">
      {isLoad && (
        <div className="flex justify-center items-center fixed top-0 left-0 z-50 bg-black bg-opacity-30 w-screen h-screen">
          <div className=" min-w-[240px]">
            <Lottie options={anim5o} />
          </div>
        </div>
      )}

      <div className="flex xs:flex-wrap gap-2 items-center mb-4">
        <div className="border transition-all duration-300 border-white rounded-3xl p-2 flex justify-center items-center">
          <div
            onClick={() => {
              setEraseMode(false);
              if (canvasRef.current) {
                canvasRef.current.eraseMode(false);
              }
            }}
            className={
              "p-1 transition-all flex justify-center items-center duration-300 rounded-full hover:cursor-pointer  " +
              (eraseMode == false ? " text-black bg-white " : "")
            }
          >
            <DrawIcon />
          </div>
          <div
            onClick={() => {
              setEraseMode(true);
              if (canvasRef.current) {
                canvasRef.current.eraseMode(true);
              }
            }}
            className={
              "p-1 transition-all flex justify-center items-center duration-300 rounded-full  text-2xl hover:cursor-pointer " +
              (eraseMode == true ? " text-black bg-white " : " ")
            }
          >
            <BiEraser />
          </div>
        </div>
        <div className="border-l border-gray-300 h-6 mx-2" />
        <div
          onClick={() => canvasRef.current && canvasRef.current.undo()}
          className="p-2 text-2xl hover:cursor-pointer"
        >
          <FaUndo />
        </div>
        <div
          onClick={() => canvasRef.current && canvasRef.current.redo()}
          className="p-2 text-2xl hover:cursor-pointer"
        >
          <FaRedo />
        </div>
        <div
          onClick={() => canvasRef.current && canvasRef.current.clearCanvas()}
          className="p-2 text-2xl hover:cursor-pointer"
        >
          <FaTrash />
        </div>
        <div
          onClick={() => canvasRef.current && canvasRef.current.resetCanvas()}
          className="p-2 text-2xl hover:cursor-pointer"
        >
          <FaSync />
        </div>
        {/* <div className="border-l border-gray-300 h-6 mx-2 " /> */}

        {/* <div
          onClick={handleUploadClick}
          className="p-2 text-2xl hover:cursor-pointer"
        >
          <FaUpload />
        </div> */}

        <div className="border-l border-gray-300 h-6 mx-2 " />
        {/* <div
          onClick={() => {
            setLoading(true);
            handleSaveClick();
          }}
          className="p-2 text-xl gap-2 flex justify-center items-center hover:cursor-pointer"
        >
          <AutoAwesomeIcon fontSize="large" />
          <div className="border transition-all text-xl duration-300  border-white rounded-3xl p-2 flex justify-center items-center">
            <div
              onClick={() => {
                setAutoCorrect(false);
              }}
              className={
                "p-1 transition-all flex justify-center  items-center w-5 aspect-square duration-300 rounded-full hover:cursor-pointer  " +
                (autoCorrect == false ? " text-black bg-white scale-125 " : "")
              }
            ></div>
            <div
              onClick={() => {
                setAutoCorrect(true);
              }}
              className={
                "p-1 transition-all flex justify-center items-center w-5 aspect-square duration-300 rounded-full  text-2xl hover:cursor-pointer " +
                (autoCorrect == true
                  ? " text-black bg-blue-500 scale-125 "
                  : " ")
              }
            ></div>
          </div>
        </div> */}
        <div
          onClick={() => {
            setLoading(true);
            //
          }}
          className="p-2 text-xl gap-2 flex justify-center items-center hover:cursor-pointer"
        >
          <AutoFixHighIcon fontSize="large" />
        </div>
        {/* <div className="border-l border-gray-300 h-6 mx-2 " /> */}
        {/* <div
          onClick={handleSaveClick}
          className="p-2 text-xl gap-2 text-nowrap font-poppins flex justify-center items-center hover:cursor-pointer"
        >
          Auto Complete
        </div> */}
        <div className="w-full flex justify-end">
          <div className="border transition-all duration-300 w-fit border-white rounded-3xl p-2 flex justify-center items-center">
            <div
              onClick={() => {
                if (mode == "black") return;
                canvasRef.current && canvasRef.current.resetCanvas();
                setMode("black");
              }}
              className={
                "p-1 transition-all duration-300 rounded-full flex justify-center items-center hover:cursor-pointer  " +
                (mode == "black" ? " text-black bg-white " : "")
              }
            >
              <LightModeIcon />
            </div>
            <div
              onClick={() => {
                if (mode == "white") return;
                canvasRef.current && canvasRef.current.resetCanvas();
                setMode("white");
              }}
              className={
                "p-1 transition-all duration-300 rounded-full flex justify-center items-center  text-2xl hover:cursor-pointer " +
                (mode == "white" ? " text-black bg-white " : " ")
              }
            >
              <NightlightRoundIcon />
            </div>
          </div>
        </div>
      </div>
      <div className="border hover:cursor-pointer rounded-lg overflow-hidden w-full h-full">
        <ReactSketchCanvas
          ref={canvasRef}
          strokeWidth={1}
          strokeColor={mode}
          canvasColor={mode == "white" ? "black" : "white"}
        />
      </div>
    </div>
  );
}
