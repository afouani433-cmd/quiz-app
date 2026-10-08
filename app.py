from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

# قاعدة بيانات مؤقتة في ذاكرة البايثون لتخزين الاختبارات
quizzes = {}

# قائمة الأسئلة المتاحة
QUESTIONS = [
    {
        "id": 1,
        "question": "لو كان فينا نشتري شي واحد غير محدود، شو بختار؟",
        "options": ["سفر حول العالم ✈️", "أكل ما بخلص 🍕", "أحدث أجهزة وتقنيات 💻", "ساعات نوم إضافية 😴"]
    },
    {
        "id": 2,
        "question": "شو أكتر شيء بيستفزني بسرعة؟",
        "options": ["النت البطئ 🌐", "التأخير عن المواعيد ⏰", "الرسائل بدون رد 📩", "الصوت العالي 🔊"]
    },
    {
        "id": 3,
        "question": "شنو بيصير لو اخترقوا جهازي؟",
        "options": ["ما حيلقوا شيء مفيد 🤷‍♂️", "حينصدموا من الملاحظات 📝", "حيلقوا 1000 صورة ألعاب 🎮", "كوارث ومحادثات غريبة 💀"]
    }
]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        creator_name = request.form.get('username')
        # تجميع إجابات صانع الاختبار
        answers = {}
        for q in QUESTIONS:
            ans_idx = request.form.get(f'q_{q["id"]}')
            if ans_idx is not None:
                answers[str(q["id"])] = int(ans_idx)
        
        # إنشاء ID فريد للرابط (مثل: 4hwkbGO)
        quiz_id = str(uuid.uuid4())[:8]
        
        # حفظ بيانات الاختبار
        quizzes[quiz_id] = {
            "creator": creator_name,
            "answers": answers
        }
        
        # توجيه المستخدم لصفحة الرابط تم إنشاؤه
        share_url = request.host_url + 'quiz/' + quiz_id
        return f'''
            <div style="text-align:center; font-family:sans-serif; margin-top:50px;">
                <h1>🎉 تم إنشاء اختبارك بنجاح يا {creator_name}!</h1>
                <p>شارك هذا الرابط مع أصدقائك:</p>
                <input type="text" value="{share_url}" style="width:300px; padding:10px; font-size:16px;" readonly>
            </div>
        '''

    return render_template('index.html', questions=QUESTIONS)


@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
def play_quiz(quiz_id):
    quiz_data = quizzes.get(quiz_id)
    if not quiz_data:
        return "<h1>عذراً، هذا الاختبار غير موجود!</h1>", 404

    if request.method == 'POST':
        friend_name = request.form.get('friend_name')
        score = 0
        total = len(QUESTIONS)

        for q in QUESTIONS:
            friend_ans = request.form.get(f'q_{q["id"]}')
            correct_ans = quiz_data['answers'].get(str(q["id"]))
            if friend_ans is not None and int(friend_ans) == correct_ans:
                score += 1

        return f'''
            <div style="text-align:center; font-family:sans-serif; margin-top:50px;">
                <h1>نتيجة التحدي لـ {friend_name} 🎉</h1>
                <h2>جبت {score} من {total} في اختبار {quiz_data['creator']}!</h2>
            </div>
        '''

    return render_template('quiz.html', quiz_id=quiz_id, creator=quiz_data['creator'], questions=QUESTIONS)

if __name__ == '__main__':
    app.run(debug=True)