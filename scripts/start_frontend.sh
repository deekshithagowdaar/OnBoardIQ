#!/usr/bin/env bash
echo "Starting OnboardIQ Frontend (Vite)..."
cd "$(dirname "$0")/../frontend" || exit
npm run dev
