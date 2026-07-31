"""
Curated skills taxonomy dictionary.
Categorized into Programming Languages, Frameworks, Cloud, Databases, DevOps, Tools, AI/ML, and Soft Skills.
"""

SKILL_TAXONOMY = {
    "programming_languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "c", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl", "dart",
        "haskell", "lua", "elixir", "clojure", "bash", "shell", "powershell", "sql", "html", "css", "sass"
    ],
    "frameworks": [
        "react", "react.js", "next.js", "vue", "vue.js", "angular", "svelte", "express",
        "express.js", "fastapi", "django", "flask", "spring", "spring boot", "ruby on rails",
        "laravel", "asp.net", ".net", "nest.js", "nestjs", "nuxt", "gatsby", "tailwind",
        "tailwind css", "bootstrap", "material-ui", "mui", "redux", "zustand", "spark", "hadoop"
    ],
    "databases": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "sqlite", "oracle",
        "mssql", "sql server", "elasticsearch", "cassandra", "dynamodb", "neo4j",
        "cockroachdb", "clickhouse", "mariadb", "firebase", "supabase", "faiss", "milvus", "chromadb"
    ],
    "cloud": [
        "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud",
        "google cloud platform", "docker", "kubernetes", "k8s", "terraform", "ansible",
        "cloudformation", "serverless", "lambda", "ec2", "s3", "ecs", "eks", "gke",
        "cloudflare", "heroku", "vercel", "digitalocean"
    ],
    "devops": [
        "git", "github", "gitlab", "bitbucket", "ci/cd", "jenkins", "github actions",
        "circleci", "travis ci", "argo", "argocd", "prometheus", "grafana", "datadog",
        "elk", "logstash", "kibana", "helm", "nginx", "apache", "traefik", "istio"
    ],
    "ai_ml": [
        "machine learning", "deep learning", "artificial intelligence", "ai", "ml",
        "nlp", "natural language processing", "computer vision", "llm", "large language models",
        "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn", "opencv", "spacy",
        "nltk", "huggingface", "transformers", "langchain", "llama", "ollama", "bert", "gpt"
    ],
    "soft_skills": [
        "leadership", "communication", "teamwork", "problem solving", "critical thinking",
        "time management", "adaptability", "collaboration", "agile", "scrum", "kanban",
        "mentorship", "project management", "negotiation", "conflict resolution", "creativity"
    ]
}

# Flat set of all canonical skill names for quick exact/case-insensitive matching
ALL_SKILLS_SET = {skill.lower() for cat in SKILL_TAXONOMY.values() for skill in cat}
