#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SHARED="$REPO_DIR/shared"

link_shared() {
  local dest="$1"
  ln -sfn "$SHARED/scripts"    "$dest/scripts"
  ln -sfn "$SHARED/references" "$dest/references"
  ln -sfn "$SHARED/assets"     "$dest/assets"
}

installed=()

# Claude Code
if command -v claude &>/dev/null || [ -d "$HOME/.claude" ]; then
  CLAUDE_SKILLS="$HOME/.claude/plugins/ai-pipeline-kit/skills"
  mkdir -p "$CLAUDE_SKILLS"
  for skill in ai-pipeline-kit run-pipeline visualize dashboard-design; do
    mkdir -p "$CLAUDE_SKILLS/$skill"
    cp "$REPO_DIR/platforms/claude/skills/$skill/SKILL.md" "$CLAUDE_SKILLS/$skill/SKILL.md"
    link_shared "$CLAUDE_SKILLS/$skill"
  done
  installed+=("Claude Code → $CLAUDE_SKILLS")
fi

# Codex
if command -v codex &>/dev/null || [ -d "$HOME/.codex" ]; then
  CODEX_PLUGIN="$HOME/.codex/plugins/ai-pipeline-kit"
  mkdir -p "$CODEX_PLUGIN"
  cp -r "$REPO_DIR/platforms/codex/." "$CODEX_PLUGIN/"
  link_shared "$CODEX_PLUGIN"
  installed+=("Codex → $CODEX_PLUGIN")
fi

# Hermes
if command -v hermes &>/dev/null || [ -d "$HOME/.hermes" ]; then
  HERMES_SKILL="$HOME/.hermes/skills/ai-pipeline-kit"
  mkdir -p "$HERMES_SKILL"
  cp "$REPO_DIR/platforms/hermes/ai-pipeline-kit/SKILL.md" "$HERMES_SKILL/SKILL.md"
  link_shared "$HERMES_SKILL"
  installed+=("Hermes → $HERMES_SKILL")
fi

# OpenClaw
if command -v openclaw &>/dev/null || [ -d "$HOME/.openclaw" ]; then
  OPENCLAW_SKILL="$HOME/.openclaw/skills/ai-pipeline-kit"
  mkdir -p "$OPENCLAW_SKILL"
  cp "$REPO_DIR/platforms/openclaw/ai-pipeline-kit/SKILL.md" "$OPENCLAW_SKILL/SKILL.md"
  link_shared "$OPENCLAW_SKILL"
  installed+=("OpenClaw → $OPENCLAW_SKILL")
fi

# Gemini CLI
if command -v gemini &>/dev/null || [ -d "$HOME/.gemini" ]; then
  GEMINI_SKILL="$HOME/.gemini/skills/ai-pipeline-kit"
  mkdir -p "$GEMINI_SKILL"
  cp "$REPO_DIR/platforms/gemini/ai-pipeline-kit/SKILL.md" "$GEMINI_SKILL/SKILL.md"
  link_shared "$GEMINI_SKILL"
  installed+=("Gemini CLI → $GEMINI_SKILL")
fi

echo ""
if [ ${#installed[@]} -eq 0 ]; then
  echo "설치된 플랫폼을 찾지 못했습니다."
  echo "수동 설치: platforms/<platform>/ 폴더를 해당 플랫폼 스킬 경로에 복사하세요."
else
  echo "설치 완료:"
  for p in "${installed[@]}"; do
    echo "  ✓ $p"
  done
fi
