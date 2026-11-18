import React from "react";
import {Composition} from "remotion";
import {BlueprintSignal} from "./BlueprintSignal";
import {DEFAULT_POST_DATA, parsePostVisualData} from "./schema";

const FPS = 30;

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="BlueprintSignalVideo"
      component={BlueprintSignal}
      width={1080}
      height={1350}
      fps={FPS}
      durationInFrames={DEFAULT_POST_DATA.durationSeconds * FPS}
      defaultProps={{...DEFAULT_POST_DATA, still: false}}
      calculateMetadata={({props}) => {
        const data = parsePostVisualData(props);
        return {durationInFrames: Math.round(data.durationSeconds * FPS)};
      }}
    />
    <Composition
      id="BlueprintSignalCover"
      component={BlueprintSignal}
      width={1080}
      height={1350}
      fps={FPS}
      durationInFrames={1}
      defaultProps={{...DEFAULT_POST_DATA, still: true}}
    />
  </>
);
