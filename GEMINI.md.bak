# 🤖 GEMINI.md - Policy และ Workflow Automation Guide

**เอกสารนี้อธิบายกฎการทำงาน (Policy) และขั้นตอนการใช้ Gemini CLI ในการจัดการ SBTU MCP Server**

---

## 📌 **หลักการทำงาน (Core Principles)**

### ✅ **1. Safety First - ลบก่อนไม่ใช่ก่อน**

```
❌ WRONG:     ✅ RIGHT:
1. ลบไฟล์      1. สร้างไฟล์ใหม่
2. สร้างใหม่   2. Test ไฟล์
3. ใช้งาน      3. ถ้า OK → ลบเก่า
```

**ปัญหาที่เกิดจากการลบก่อน:**
- ไฟล์เก่าหายไปถ้าไฟล์ใหม่มีปัญหา
- ไม่มี backup/recovery
- เสียเวลาสูงในการ restore

**วิธีที่ถูก:**
1. ✅ เพิ่มไฟล์ใหม่ ใช้ชื่อใหม่ (เช่น `proxy_v2.py` แทน `proxy.py`)
2. ✅ Test ให้แน่ใจว่าทำงานได้
3. ✅ ถ้า OK → ลบไฟล์เก่า
4. ✅ Rename ไฟล์ใหม่เป็นชื่อเดิม

---

### ✅ **2. Backup Before Delete**

```bash
# Step 1: Create backup
cp existing_file.py existing_file.py.bak

# Step 2: Create new version
# (edit or create new file)

# Step 3: Test new version
python existing_file.py --test

# Step 4: If OK, delete backup
rm existing_file.py.bak

# Step 5: If NOT OK, restore
cp existing_file.py.bak existing_file.py
```

---

### ✅ **3. Test Before Push**

```bash
# Step 1: Make changes locally
# (edit files, create new code)

# Step 2: Test locally
pytest src/ -v
flake8 src/
python -m src.module --test

# Step 3: Only push if tests pass
git push origin main
```

---

## 📋 **Workflow สำหรับ Gemini CLI**

### **ขั้น 1: Understanding Current State**

```bash
# ตรวจสอบไฟล์ปัจจุบัน
git status

# ดูประวัติการเปลี่ยนแปลง
git log --oneline -10

# เปิดไฟล์เดิมดูก่อนแก้ไข
cat existing_file.py
```

### **ขั้น 2: Create New Version (Don't Delete Yet)**

```bash
# สร้างไฟล์ใหม่ หรือแก้ไข
# ชื่อใหม่: modified_file.py (แทนการลบ existing_file.py)

# หรือสร้าง branch ใหม่
git checkout -b feature/update-file
```

### **ขั้น 3: Test Thoroughly**

```bash
# Test code
python modified_file.py --test

# Run unit tests
pytest src/ -v

# Check syntax
python -m py_compile modified_file.py

# If everything OK, proceed to step 4
# If NOT OK, fix or revert
```

### **ขั้น 4: Safe Replacement**

```bash
# Option A: If new file works, replace old
cp existing_file.py existing_file.py.bak
cp modified_file.py existing_file.py

# Option B: Or just remove the old one after confirming new works
rm existing_file.py
mv modified_file.py existing_file.py
```

### **ขั้น 5: Commit and Push**

```bash
git add .
git commit -m "feat: update existing_file with new implementation"
git push origin feature/update-file
```

---

## 🚨 **Common Mistakes to Avoid**

### ❌ **Mistake 1: Delete then Create**
```bash
# ❌ BAD
rm important_file.py
# ... create new file ...
# 💥 If error happens, file is gone!
```

### ❌ **Mistake 2: No Testing**
```bash
# ❌ BAD
git push origin main
# CI/CD fails, but old file already deleted
```

### ❌ **Mistake 3: Complex Command Substitution**
```bash
# ❌ BAD - Can fail silently
RESULT=$(complex-command) && rm file.py

# ✅ GOOD - Separate steps
RESULT=$(complex-command)
if [ $? -eq 0 ]; then
    rm file.py
fi
```

---

## ✅ **Best Practices for Gemini CLI**

### **Pattern 1: File Modification**

```markdown
**Scenario:** Update existing Python file

**Steps:**
1. Read the existing file content
2. Understand what it does
3. Create modified version with clear changes
4. Show the diff clearly
5. Test locally
6. Only delete old file after confirmation
```

### **Pattern 2: Adding New Features**

```markdown
**Scenario:** Add new feature/module

**Steps:**
1. Create new file with feature-branch naming (e.g., feature_xyz.py)
2. Implement feature completely
3. Add tests for the feature
4. Push to feature branch
5. Create Pull Request
6. Wait for review and tests
7. Merge to main only after approval
```

### **Pattern 3: Bug Fix**

```markdown
**Scenario:** Fix bug in existing code

**Steps:**
1. Create backup: `cp buggy_file.py buggy_file.py.bak`
2. Fix the bug
3. Run tests: `pytest -k bug_test`
4. If tests pass, delete backup
5. Commit with message: `fix: describe the bug`
```

---

## 📊 **Decision Tree**

```
┌─ Start
│
├─ Need to modify file?
│  ├─ YES → Create modified version (don't delete yet)
│  └─ NO → Skip to Push
│
├─ Test passed?
│  ├─ YES → Replace old file
│  └─ NO → Fix or revert, re-test
│
├─ Delete old file?
│  ├─ YES → Delete backup
│  └─ NO → Keep for recovery
│
└─ Push to GitHub
   └─ End
```

---

## 🔧 **Script Templates for Gemini CLI**

### **Template 1: Safe File Update**

```bash
#!/bin/bash
set -e  # Exit on error

FILE_NAME="my_file.py"

echo "1️⃣ Backing up existing file..."
cp "$FILE_NAME" "$FILE_NAME.bak"

echo "2️⃣ Creating new version..."
# (Gemini creates new code here)
cat > "$FILE_NAME" << 'EOF'
# New code goes here
def my_function():
    pass
EOF

echo "3️⃣ Testing new version..."
if python -m py_compile "$FILE_NAME"; then
    echo "✅ New file compiles OK"
    echo "4️⃣ Removing backup..."
    rm "$FILE_NAME.bak"
else
    echo "❌ New file has errors, restoring backup..."
    cp "$FILE_NAME.bak" "$FILE_NAME"
    exit 1
fi

echo "5️⃣ Committing changes..."
git add "$FILE_NAME"
git commit -m "feat: update $FILE_NAME"
git push origin main

echo "🎉 Update complete!"
```

### **Template 2: Commit Message Convention**

```
feat: Add new feature/module
fix: Fix bug in module
docs: Update documentation
refactor: Improve code structure
test: Add or update tests
chore: Update dependencies/config
```

**Example:**
```
feat: Add GitHub API integration module
fix: Resolve token validation error in proxy
docs: Update CONTRIBUTING.md with new workflow
```

---

## 📝 **Checklist ก่อน Push**

- ✅ ไฟล์เก่ายังมีหรือไม่ (ถ้าจำเป็นต้องลบ)
- ✅ ไฟล์ใหม่ test ผ่านแล้วไหม
- ✅ ไม่มี syntax errors
- ✅ ไม่มี breaking changes (หรือ documented properly)
- ✅ Commit message ชัดเจน
- ✅ Ready to push!

---

## 📞 **สำหรับ Gemini CLI**

เมื่อใช้ Gemini CLI ให้จำ:

```
1. 🔍 READ the existing code first
2. 🛡️ BACKUP before deleting
3. 🧪 TEST after creating
4. 📝 DOCUMENT what changed
5. 🚀 PUSH only when safe
```

**นี่คือ "Software Craftsmanship" ครับ** 🎯

