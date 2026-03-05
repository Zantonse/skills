# Component Patterns Reference

## Shared Layout Animation Dialog (React + Motion + Radix)

Two separate components animate into each other using `layoutId`:

```tsx
import { motion, AnimatePresence } from "motion/react";
import * as Dialog from "@radix-ui/react-dialog";

function CardToDialog({ item }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <motion.div layoutId={`card-${item.id}`} onClick={() => setOpen(true)}
        className="cursor-pointer rounded-xl p-4"
        style={{ boxShadow: "var(--shadow-border)" }}>
        <motion.h3 layoutId={`title-${item.id}`}>{item.title}</motion.h3>
      </motion.div>
      <Dialog.Root open={open} onOpenChange={setOpen}>
        <AnimatePresence>
          {open && (
            <Dialog.Portal forceMount>
              <Dialog.Overlay asChild>
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }} className="fixed inset-0 bg-black/20" />
              </Dialog.Overlay>
              <Dialog.Content asChild>
                <motion.div layoutId={`card-${item.id}`}
                  className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rounded-2xl bg-white p-6"
                  style={{ boxShadow: "var(--shadow-elevated)" }}>
                  <motion.h3 layoutId={`title-${item.id}`}>{item.title}</motion.h3>
                  <p>{item.description}</p>
                </motion.div>
              </Dialog.Content>
            </Dialog.Portal>
          )}
        </AnimatePresence>
      </Dialog.Root>
    </>
  );
}
```

## Animated Icon Transitions

Animate opacity, scale, and blur when swapping icons contextually:

```tsx
function AnimatedIcon({ icon: Icon, key }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div key={key}
        initial={{ opacity: 0, scale: 0.8, filter: "blur(4px)" }}
        animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
        exit={{ opacity: 0, scale: 0.8, filter: "blur(4px)" }}
        transition={{ duration: 0.15 }}>
        <Icon className="w-5 h-5" />
      </motion.div>
    </AnimatePresence>
  );
}
```

## Infinite Card Stack with Drag Gesture

```tsx
function CardStack({ items }) {
  const [stack, setStack] = useState(items);
  return (
    <div className="relative h-64 w-48">
      {stack.slice(0, 3).map((item, i) => (
        <motion.div key={item.id}
          drag={i === 0 ? "x" : false}
          dragConstraints={{ left: 0, right: 0 }}
          onDragEnd={(_, info) => {
            if (Math.abs(info.offset.x) > 100) {
              setStack(prev => [...prev.slice(1), prev[0]]);
            }
          }}
          style={{
            position: "absolute", inset: 0,
            zIndex: stack.length - i,
            scale: 1 - i * 0.05,
            y: i * 8,
            boxShadow: "var(--shadow-border)",
          }}
          className="rounded-xl bg-white p-4"
          whileDrag={{ scale: 1.02, rotate: info => info.offset.x * 0.05 }}>
          {item.content}
        </motion.div>
      ))}
    </div>
  );
}
```

## Animated Tab Indicator

```tsx
function Tabs({ items, active, onChange }) {
  return (
    <div className="flex gap-1 relative">
      {items.map(item => (
        <button key={item} onClick={() => onChange(item)}
          className="relative px-4 py-2 text-sm font-medium z-10"
          style={{ color: active === item ? "#FCFCFC" : "#202020" }}>
          {active === item && (
            <motion.div layoutId="tab-indicator"
              className="absolute inset-0 rounded-lg bg-[#202020]"
              style={{ zIndex: -1 }}
              transition={{ type: "spring", stiffness: 400, damping: 30 }} />
          )}
          {item}
        </button>
      ))}
    </div>
  );
}
```

## SVG Path Drawing Animation

```tsx
function DrawIcon() {
  return (
    <motion.svg viewBox="0 0 24 24" className="w-6 h-6">
      <motion.path
        d="M5 13l4 4L19 7"
        fill="none" stroke="#202020" strokeWidth={2}
        strokeLinecap="round" strokeLinejoin="round"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 0.4, ease: "easeInOut" }} />
    </motion.svg>
  );
}
```

## Input Field with Animated Label

```tsx
function AnimatedInput({ label, ...props }) {
  const [focused, setFocused] = useState(false);
  const [value, setValue] = useState("");
  const isActive = focused || value.length > 0;
  return (
    <div className="relative" style={{ boxShadow: focused ? "var(--shadow-medium)" : "var(--shadow-border)" }}>
      <motion.label
        animate={{ y: isActive ? -12 : 0, scale: isActive ? 0.85 : 1 }}
        className="absolute left-3 top-3 origin-left pointer-events-none"
        style={{ color: "oklch(0.55 0 0)" }}>
        {label}
      </motion.label>
      <input {...props} value={value}
        onChange={e => setValue(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        className="w-full px-3 pt-5 pb-2 rounded-lg bg-white outline-none" />
    </div>
  );
}
```

## Outline Orbit Button Effect

A button with multiple outlines that orbit around it using conic-gradient animation:

```css
.orbit-btn {
  position: relative;
  padding: 10px 20px;
  background: #202020;
  color: #FCFCFC;
  border-radius: 8px;
  border: none;
}
.orbit-btn::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 10px; /* concentric: 8px + 2px */
  background: conic-gradient(from var(--angle, 0deg),
    transparent 0deg, oklch(0.7 0.15 250) 30deg,
    transparent 60deg, transparent 360deg);
  animation: orbit 3s linear infinite;
  z-index: -1;
}
@keyframes orbit { to { --angle: 360deg; } }
/* Requires @property --angle registration */
@property --angle { syntax: "<angle>"; initial-value: 0deg; inherits: false; }
```
