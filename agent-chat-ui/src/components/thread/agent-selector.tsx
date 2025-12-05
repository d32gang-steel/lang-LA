"use client";

import { useQueryState } from "nuqs";
import { Button } from "../ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "../ui/tooltip";
import { ChevronDown } from "lucide-react";
import { useState, useRef, useEffect } from "react";

const AGENTS = [
  { id: "compute-agent", name: "计算助手", description: "执行线性代数计算" },
  { id: "visual-agent", name: "可视化助手", description: "生成线性变换图像" },
  { id: "socratic-agent", name: "苏格拉底式教学", description: "通过提问引导学习" },
] as const;

export function AgentSelector() {
  const [assistantId, setAssistantId] = useQueryState("assistantId");
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  const currentAgent =
    AGENTS.find((a) => a.id === assistantId) || AGENTS[0];

  const handleSelect = (agentId: string) => {
    setIsOpen(false);
    // Reset thread when switching agents by clearing threadId
    const url = new URL(window.location.href);
    url.searchParams.set("assistantId", agentId);
    url.searchParams.delete("threadId");
    // Navigate to new URL, which will reset the stream context
    window.location.href = url.toString();
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="outline"
              className="flex items-center gap-2"
              onClick={() => setIsOpen(!isOpen)}
            >
              <span className="text-sm font-medium">{currentAgent.name}</span>
              <ChevronDown
                className={`h-4 w-4 transition-transform ${
                  isOpen ? "rotate-180" : ""
                }`}
              />
            </Button>
          </TooltipTrigger>
          <TooltipContent side="bottom">
            <p>切换 Agent</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>

      {isOpen && (
        <div className="absolute right-0 top-full z-50 mt-2 w-56 rounded-md border bg-white shadow-lg">
          <div className="p-1">
            {AGENTS.map((agent) => (
              <button
                key={agent.id}
                onClick={() => handleSelect(agent.id)}
                className={`w-full rounded-sm px-3 py-2 text-left text-sm transition-colors ${
                  assistantId === agent.id
                    ? "bg-gray-100 font-medium"
                    : "hover:bg-gray-50"
                }`}
              >
                <div className="font-medium">{agent.name}</div>
                <div className="text-xs text-gray-500">
                  {agent.description}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

