# 🔥 Resume Roaster AI

<p align="center">
  <img src="./logo.png" width="600" alt="Project Logo" />
</p>

We trained an SLM (Small Language Model) assistant for automatic resume critique — a Llama-3.2-3B parameter model that generates "Roast Mode" feedback and professional improvement suggestions.
Run it locally to keep your personal data private, or deploy it for instant feedback!


### **1. Install Dependencies**

First, install **[Ollama](http://ollama.com/)** from their official website.  
Then set up your Python environment:

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install required tools
pip install huggingface_hub ollama rich pymupdf
```
Available models hosted on HuggingFace:

- **[Priyansu19/Distil-Rost-Resume-Llama-3.2-3B-Instruct](https://huggingface.co/Priyansu19/Distil-Rost-Resume-Llama-3.2-3B-Instruct)**

### **2. Setup the Model**

Download your fine-tuned GGUF model and register it with Ollama.

```bash
hf download Priyansu19/Distil-Rost-Resume-Llama-3.2-3B-Instruct --local-dir distil-model

cd distil-model
# Create the Ollama model from the Modelfile
ollama create roast_master -f Modelfile
```
> **Note:**  
> If the command above fails with **"Modelfile not found"**, create a file named **`Modelfile`** inside the `distil-model` folder with the following content:

```dockerfile
FROM ./unsloth.Q4_K_M.gguf
PARAMETER stop "<|start_header_id|>"
PARAMETER stop "<|end_header_id|>"
PARAMETER stop "<|eot_id|>"


### **3. Usage**

Now you can roast any resume PDF instantly from your terminal.

```bash
# Syntax: python roast.py <path_to_resume.pdf>
python roast.py my_resume.pdf
```

## ✨ Features

The assistant is trained to analyze resumes and output structured JSON containing:

- **💀 Roast Critique**  
  A sarcastic, humorous paragraph quoting specific problematic parts of the resume (typos, clichés, gaps).

- **✨ Professional Suggestions**  
  A list of **exactly 3** constructive, actionable tips to improve the resume.

- **📊 Rating**  
  An integer score **(1–10)** based on overall resume quality.
  

### **Examples**

---

#### 🟦 Example 1
<p align="center">
  <img src="./examples/ex-1.png" width="550" alt="Example 1" />
</p>

---

#### 🟩 Example 2
<p align="center">
  <img src="./examples/ex-2.png" width="550" alt="Example 2" />
</p>

## 📊 Performance

We benchmarked our student model against the teacher (**Llama 3.3 70B**).  
The fine-tuned **3B student model** achieves perfect format compliance and captures the **Roast persona** effectively.

---

### **Evaluation Metrics**

| **Metric**         | **Teacher (70B)** | **Student-Base (Untrained)** | **Student-Tuned (Ours)** |
|--------------------|-------------------|-------------------------------|---------------------------|
| **ROUGE-L**        | 0.21              | 0.16                          | **0.23 ⬆** |
| **METEOR**         | 0.32              | 0.27                          | **0.35 ⬆** |
| **LLM-as-a-Judge** | **1.00**          | 0.13                          | **1.00 ⬆** |

> **Note:**  
> A **1.00 LLM-as-a-Judge** score indicates the model perfectly follows the complex JSON schema and Roast persona instructions.

---

### **Training Config**

- **Student:** Llama-3.2-3B-Instruct  
- **Teacher:** openai.gpt-oss-120b 
- **Dataset:** 10,000 synthetic examples

## ❓ FAQ

---

<details>
<summary><strong>Q: Why not just use ChatGPT or Claude?</strong></summary>

**Privacy and cost.**  
Resumes contain sensitive personal data (PII). Sending them to cloud APIs risks exposure.  
Our model runs **fully locally**, ensuring zero data leaks and costs **nothing** to run.
</details>

---

<details>
<summary><strong>Q: How accurate is a 3B model compared to GPT-4?</strong></summary>

Surprisingly good for this specific task!  
Because it’s fine-tuned on **6,000+ high-quality roast-style examples**, it performs far better than a generic prompt to GPT-4.  
It captures the **roast persona** more consistently and is extremely fast.
</details>

---

<details>
<summary><strong>Q: Can I use this for serious resume reviews?</strong></summary>

Yes!  
The **Professional Suggestions** section is trained on real career guidance data.  
You can ignore the roast and only use the actionable tips.
</details>

---

<details>
<summary><strong>Q: The model is too mean! Can I change it?</strong></summary>

The model is intentionally “brutally honest.”  
But since it outputs **structured JSON**, you can simply hide the `roast` field and show only the suggestions.
</details>

---

<details>
<summary><strong>Q: What hardware do I need?</strong></summary>

**Minimum:**  
- 8GB RAM (CPU Mode)  
- Works well on modern laptops (Mac M1/M2/M3 recommended)

**Recommended:**  
- NVIDIA GPU with **4GB+ VRAM** for 2–5s inference  
</details>

---

## 🤝 Community

Stay connected with Distil Labs and explore our ecosystem:

<p align="left">
  <a href="https://www.linkedin.com/company/distil-labs/posts/?feedView=all">
    <img src="https://img.shields.io/badge/LinkedIn-Follow%20Us-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge" />
  </a>

  <a href="https://www.distillabs.ai/">
    <img src="https://img.shields.io/badge/Website-Distil%20Labs-111111?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website Badge" />
  </a>

  <a href="https://huggingface.co/distil-labs">
    <img src="https://img.shields.io/badge/HuggingFace-Models-FFCC4D?style=for-the-badge&logo=huggingface&logoColor=black" alt="HuggingFace Badge" />
  </a>

  <a href="https://www.distillabs.ai/contact">
    <img src="https://img.shields.io/badge/Contact-Get%20in%20Touch-00C853?style=for-the-badge&logo=gmail&logoColor=white" alt="Contact Badge" />
  </a>

  <a href="https://distil-labs-community.slack.com/ssb/redirect">
    <img src="https://img.shields.io/badge/Slack-Join%20Community-4A154B?style=for-the-badge&logo=slack&logoColor=white" alt="Slack Badge" />
  </a>
</p>




