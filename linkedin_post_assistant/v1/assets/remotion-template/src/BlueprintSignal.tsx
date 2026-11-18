import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {parsePostVisualData, type PostVisualData} from "./schema";

type BlueprintSignalProps = PostVisualData & {still?: boolean};

const COLORS = {
  background: "#edf5ff",
  navy: "#10233f",
  blue: "#1464c8",
  grid: "rgba(69, 119, 178, 0.18)",
  white: "#f8fbff",
  muted: "#49627f",
};

const reveal = (frame: number, fps: number, delay: number, still: boolean) => {
  if (still) return 1;
  return spring({frame: frame - delay, fps, config: {damping: 18, stiffness: 120}});
};

const Reveal: React.FC<{
  progress: number;
  children: React.ReactNode;
  shift?: number;
}> = ({progress, children, shift = 24}) => (
  <div
    style={{
      opacity: interpolate(progress, [0, 1], [0, 1]),
      transform: `translateY(${interpolate(progress, [0, 1], [shift, 0])}px)`,
    }}
  >
    {children}
  </div>
);

export const BlueprintSignal: React.FC<BlueprintSignalProps> = (props) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const data = parsePostVisualData(props);
  const still = props.still === true;
  const headlineProgress = reveal(frame, fps, 4, still);
  const flowProgress = reveal(frame, fps, 28, still);
  const supportingProgress = reveal(frame, fps, 55, still);
  const footerProgress = reveal(frame, fps, 75, still);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: COLORS.background,
        color: COLORS.navy,
        fontFamily: "Inter, Arial, Helvetica, sans-serif",
        padding: 80,
        justifyContent: "space-between",
        backgroundImage: `linear-gradient(${COLORS.grid} 1px, transparent 1px), linear-gradient(90deg, ${COLORS.grid} 1px, transparent 1px)`,
        backgroundSize: "24px 24px",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          color: COLORS.blue,
          fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace",
          fontWeight: 700,
          fontSize: 26,
          letterSpacing: 3,
        }}
      >
        <span>{data.series}</span>
        <span>{data.issue}</span>
      </div>

      <div style={{display: "flex", flexDirection: "column", gap: 56}}>
        <Reveal progress={headlineProgress}>
          <div
            style={{
              fontSize: 78,
              lineHeight: 0.98,
              fontWeight: 750,
              letterSpacing: -4,
              maxWidth: 900,
              overflowWrap: "anywhere",
              wordBreak: "break-word",
            }}
          >
            {data.headline}
          </div>
        </Reveal>

        <Reveal progress={flowProgress}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              flexWrap: "wrap",
              gap: 18,
              fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace",
              fontSize: 25,
              fontWeight: 700,
            }}
          >
            {data.nodes.map((node, index) => (
              <React.Fragment key={`${node}-${index}`}>
                <div
                  style={{
                    color: COLORS.white,
                    background: COLORS.navy,
                    borderRadius: 12,
                    padding: "22px 25px",
                    maxWidth: 360,
                    overflowWrap: "anywhere",
                    wordBreak: "break-word",
                  }}
                >
                  {node}
                </div>
                {index < data.nodes.length - 1 ? (
                  <span aria-hidden style={{color: COLORS.blue, fontSize: 38}}>
                    →
                  </span>
                ) : null}
              </React.Fragment>
            ))}
          </div>
        </Reveal>

        <Reveal progress={supportingProgress}>
          <div
            style={{
              maxWidth: 850,
              color: COLORS.muted,
              fontSize: 38,
              lineHeight: 1.25,
              fontWeight: 500,
              overflowWrap: "anywhere",
              wordBreak: "break-word",
            }}
          >
            {data.supportingText}
          </div>
        </Reveal>
      </div>

      <Reveal progress={footerProgress} shift={14}>
        <div
          style={{
            color: COLORS.blue,
            fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace",
            fontWeight: 750,
            fontSize: 28,
            letterSpacing: 2,
            maxWidth: 920,
            overflowWrap: "anywhere",
            wordBreak: "break-word",
          }}
        >
          {data.footer}
        </div>
      </Reveal>
    </AbsoluteFill>
  );
};
