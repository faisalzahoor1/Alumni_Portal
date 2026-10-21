import { initials } from "@/lib/utils/formatters";

export default function Avatar({ name, src, size = 40 }) {
  return (
    <span className="avatar" style={{ width: size, height: size, fontSize: size * 0.38 }}>
      {src ? <img src={src} alt={name || "avatar"} /> : initials(name) || "?"}
    </span>
  );
}
