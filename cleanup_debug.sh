#!/bin/bash
# Cleanup script for debug folders created by dice_complete.py

echo "🧹 Debug Folder Cleanup Script"
echo "=============================="
echo ""

# Count debug folders
debug_folders=$(ls -d debug_* 2>/dev/null | wc -l)

if [ $debug_folders -eq 0 ]; then
    echo "✅ No debug folders found to clean up"
    exit 0
fi

echo "📁 Found $debug_folders debug folder(s):"
ls -lhd debug_*/
echo ""

# Calculate total size
total_size=$(du -sh debug_* 2>/dev/null | awk '{sum+=$1} END {print sum}')
echo "💾 Total size: ~$(du -sh debug_* 2>/dev/null | awk '{s+=$1}END{print s}') MB"
echo ""

# Ask for confirmation
read -p "⚠️  Delete all debug folders? (y/N): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    echo ""
    echo "🗑️  Deleting debug folders..."
    rm -rf debug_*
    echo "✅ All debug folders deleted!"
else
    echo ""
    echo "❌ Cleanup cancelled"
fi
