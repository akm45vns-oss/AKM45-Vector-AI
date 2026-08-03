"use client";

import React, { useEffect, useRef } from "react";

export interface NeuralBgProps {
  hue?: number;
  saturation?: number;
  chroma?: number;
  speed?: number;
  particleCount?: number;
  className?: string;
  children?: React.ReactNode;
}

interface Node {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  baseRadius: number;
  pulseSpeed: number;
  pulsePhase: number;
}

interface PulseSignal {
  fromNode: number;
  toNode: number;
  progress: number;
  speed: number;
}

export const NeuralBg: React.FC<NeuralBgProps> = ({
  hue = 200,
  saturation = 0.8,
  chroma = 0.6,
  speed = 1.0,
  particleCount = 65,
  className = "",
  children,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let width = (canvas.width = canvas.parentElement?.clientWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.clientHeight || 600);

    const nodes: Node[] = [];
    const pulses: PulseSignal[] = [];
    const mouse = { x: -1000, y: -1000 };

    // Initialize Nodes
    const count = Math.min(particleCount, Math.floor((width * height) / 12000));
    for (let i = 0; i < count; i++) {
      nodes.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.8 * speed,
        vy: (Math.random() - 0.5) * 0.8 * speed,
        radius: Math.random() * 2.5 + 1.5,
        baseRadius: Math.random() * 2.5 + 1.5,
        pulseSpeed: Math.random() * 0.03 + 0.01,
        pulsePhase: Math.random() * Math.PI * 2,
      });
    }

    const handleResize = () => {
      if (!canvas || !canvas.parentElement) return;
      width = canvas.width = canvas.parentElement.clientWidth || window.innerWidth;
      height = canvas.height = canvas.parentElement.clientHeight || 600;
    };

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    };

    const handleMouseLeave = () => {
      mouse.x = -1000;
      mouse.y = -1000;
    };

    window.addEventListener("resize", handleResize);
    canvas.parentElement?.addEventListener("mousemove", handleMouseMove);
    canvas.parentElement?.addEventListener("mouseleave", handleMouseLeave);

    const maxDist = 140;
    const satPct = Math.round(saturation * 100);
    const lightPct = Math.round(chroma * 80);

    // Animation Loop
    const draw = () => {
      ctx.clearRect(0, 0, width, height);

      // Radial background glow matching hue
      const bgGlow = ctx.createRadialGradient(
        width / 2,
        height / 2,
        10,
        width / 2,
        height / 2,
        Math.max(width, height) / 1.2
      );
      bgGlow.addColorStop(0, `hsla(${hue}, ${satPct}%, 12%, 0.45)`);
      bgGlow.addColorStop(0.5, `hsla(${hue + 20}, ${satPct}%, 7%, 0.3)`);
      bgGlow.addColorStop(1, `hsla(${hue}, ${satPct}%, 3%, 0.1)`);
      ctx.fillStyle = bgGlow;
      ctx.fillRect(0, 0, width, height);

      // Update and draw connections (Synapses)
      for (let i = 0; i < nodes.length; i++) {
        const nodeA = nodes[i];

        // Move node
        nodeA.x += nodeA.vx;
        nodeA.y += nodeA.vy;

        // Bounce walls
        if (nodeA.x < 0 || nodeA.x > width) nodeA.vx *= -1;
        if (nodeA.y < 0 || nodeA.y > height) nodeA.vy *= -1;

        // Mouse attraction
        const dxMouse = mouse.x - nodeA.x;
        const dyMouse = mouse.y - nodeA.y;
        const distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
        if (distMouse < 180) {
          nodeA.x += (dxMouse / distMouse) * 0.6;
          nodeA.y += (dyMouse / distMouse) * 0.6;
          nodeA.radius = nodeA.baseRadius + (1 - distMouse / 180) * 3;
        } else {
          nodeA.radius = nodeA.baseRadius;
        }

        // Draw connections to nearby nodes
        for (let j = i + 1; j < nodes.length; j++) {
          const nodeB = nodes[j];
          const dx = nodeB.x - nodeA.x;
          const dy = nodeB.y - nodeA.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < maxDist) {
            const alpha = (1 - dist / maxDist) * 0.55;
            ctx.beginPath();
            ctx.moveTo(nodeA.x, nodeA.y);
            ctx.lineTo(nodeB.x, nodeB.y);
            ctx.strokeStyle = `hsla(${hue + (dist / maxDist) * 30}, ${satPct}%, ${lightPct}%, ${alpha})`;
            ctx.lineWidth = (1 - dist / maxDist) * 1.5;
            ctx.stroke();

            // Randomly spawn traveling impulse pulse
            if (Math.random() < 0.0015) {
              pulses.push({
                fromNode: i,
                toNode: j,
                progress: 0,
                speed: 0.02 + Math.random() * 0.02,
              });
            }
          }
        }
      }

      // Update and draw traveling synaptic pulses
      for (let p = pulses.length - 1; p >= 0; p--) {
        const pulse = pulses[p];
        pulse.progress += pulse.speed;

        if (pulse.progress >= 1) {
          pulses.splice(p, 1);
          continue;
        }

        const nodeA = nodes[pulse.fromNode];
        const nodeB = nodes[pulse.toNode];
        if (!nodeA || !nodeB) continue;

        const px = nodeA.x + (nodeB.x - nodeA.x) * pulse.progress;
        const py = nodeA.y + (nodeB.y - nodeA.y) * pulse.progress;

        const pGlow = ctx.createRadialGradient(px, py, 0, px, py, 8);
        pGlow.addColorStop(0, `hsla(${hue + 40}, 100%, 85%, 0.95)`);
        pGlow.addColorStop(0.5, `hsla(${hue}, 100%, 65%, 0.6)`);
        pGlow.addColorStop(1, `hsla(${hue}, 100%, 50%, 0)`);

        ctx.beginPath();
        ctx.arc(px, py, 8, 0, Math.PI * 2);
        ctx.fillStyle = pGlow;
        ctx.fill();
      }

      // Draw Nodes (Neurons)
      for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];
        node.pulsePhase += node.pulseSpeed;
        const currentRadius = node.radius + Math.sin(node.pulsePhase) * 0.8;

        const nGlow = ctx.createRadialGradient(
          node.x,
          node.y,
          0,
          node.x,
          node.y,
          currentRadius * 4
        );
        nGlow.addColorStop(0, `hsla(${hue}, 100%, 75%, 0.9)`);
        nGlow.addColorStop(0.4, `hsla(${hue}, ${satPct}%, ${lightPct}%, 0.5)`);
        nGlow.addColorStop(1, `hsla(${hue}, ${satPct}%, 30%, 0)`);

        ctx.beginPath();
        ctx.arc(node.x, node.y, currentRadius * 4, 0, Math.PI * 2);
        ctx.fillStyle = nGlow;
        ctx.fill();

        ctx.beginPath();
        ctx.arc(node.x, node.y, currentRadius, 0, Math.PI * 2);
        ctx.fillStyle = `hsl(${hue + 20}, 100%, 85%)`;
        ctx.fill();
      }

      animId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      window.removeEventListener("resize", handleResize);
      if (canvas?.parentElement) {
        canvas.parentElement.removeEventListener("mousemove", handleMouseMove);
        canvas.parentElement.removeEventListener("mouseleave", handleMouseLeave);
      }
      cancelAnimationFrame(animId);
    };
  }, [hue, saturation, chroma, speed, particleCount]);

  return (
    <div className={`relative w-full min-h-screen overflow-hidden ${className}`}>
      <canvas
        ref={canvasRef}
        className="fixed inset-0 w-full h-full pointer-events-none z-0 opacity-90"
      />
      {children && <div className="relative z-10 w-full">{children}</div>}
    </div>
  );
};

export default NeuralBg;
