const INTRO_KEY = "fx-intro-seen";

// Runs before first paint so the intro shows once per browser session, never on repeat navigations.
export const introScript = `try{if(!sessionStorage.getItem("${INTRO_KEY}")&&!matchMedia("(prefers-reduced-motion: reduce)").matches){document.documentElement.dataset.intro="1";sessionStorage.setItem("${INTRO_KEY}","1")}}catch(e){}`;

export default function Intro({ label }) {
  return (
    <div className="fx-intro" aria-hidden>
      <div className="fx-intro-panel fx-intro-top" />
      <div className="fx-intro-panel fx-intro-bottom" />
      <div className="fx-intro-ring" />
      <div className="fx-intro-word">
        {[...label].map((char, i) => (
          <span key={i} style={{ "--i": i }}>
            {char === " " ? " " : char}
          </span>
        ))}
      </div>
    </div>
  );
}
