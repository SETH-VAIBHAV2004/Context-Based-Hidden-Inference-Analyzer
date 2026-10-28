import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <nav className="border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="text-xl font-semibold text-gray-900">
              Inferring the Unsaid
            </div>
            <div className="flex space-x-8">
              <Link href="/" className="text-gray-700 hover:text-gray-900">Overview</Link>
              <Link href="/workbench" className="text-gray-700 hover:text-gray-900">Workbench</Link>
              <Link href="/experiments" className="text-gray-700 hover:text-gray-900">Experiments</Link>
              <Link href="/datasets" className="text-gray-700 hover:text-gray-900">Datasets</Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="space-y-12">
          {/* Hero Section */}
          <section className="border-b border-gray-200 pb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Explainable Context-Aware Pragmatic Reasoning
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed">
              A research platform for analyzing multi-turn conversations, predicting implied speaker intent,
              and providing evidence-based explanations of pragmatic inference.
            </p>
          </section>

          {/* Research Objective */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Research Objective</h2>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 space-y-4">
              <p className="text-gray-700 leading-relaxed">
                <strong>Hypothesis:</strong> Combining multi-turn conversational context with explicit
                linguistic features and evidence-based explanations can improve pragmatic inference and
                make model predictions more interpretable.
              </p>
              <p className="text-gray-700 leading-relaxed">
                <strong>Approach:</strong> We integrate multi-turn context modeling with explainable
                evidence generation for pragmatic inference in a single pipeline, extending beyond
                classification-only or single-turn prior work.
              </p>
              <p className="text-sm text-gray-600 italic">
                This is a hypothesis to evaluate, not an established result.
              </p>
            </div>
          </section>

          {/* System Pipeline */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">System Pipeline</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="text-sm font-medium text-indigo-600 mb-2">1. Input</div>
                <div className="text-sm text-gray-700">Multi-turn conversation with target utterance</div>
              </div>
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="text-sm font-medium text-indigo-600 mb-2">2. Context</div>
                <div className="text-sm text-gray-700">Extract context window and linguistic features</div>
              </div>
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="text-sm font-medium text-indigo-600 mb-2">3. Inference</div>
                <div className="text-sm text-gray-700">Predict pragmatic interpretation</div>
              </div>
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="text-sm font-medium text-indigo-600 mb-2">4. Evidence</div>
                <div className="text-sm text-gray-700">Generate and evaluate supporting evidence</div>
              </div>
            </div>
          </section>

          {/* Models */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Models</h2>
            <div className="space-y-3">
              <div className="border border-gray-200 rounded-lg p-4 flex justify-between items-center">
                <div>
                  <div className="font-medium text-gray-900">TF-IDF + Logistic Regression</div>
                  <div className="text-sm text-gray-600">Interpretable baseline with context ablations</div>
                </div>
                <span className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded">Baseline</span>
              </div>
              <div className="border border-gray-200 rounded-lg p-4 flex justify-between items-center">
                <div>
                  <div className="font-medium text-gray-900">Transformer Baseline</div>
                  <div className="text-sm text-gray-600">Fine-tuned encoder on target utterance only</div>
                </div>
                <span className="text-xs px-2 py-1 bg-yellow-100 text-yellow-700 rounded">Planned</span>
              </div>
              <div className="border border-gray-200 rounded-lg p-4 flex justify-between items-center">
                <div>
                  <div className="font-medium text-gray-900">Context-Aware Transformer</div>
                  <div className="text-sm text-gray-600">Multi-turn context with explicit target marking</div>
                </div>
                <span className="text-xs px-2 py-1 bg-yellow-100 text-yellow-700 rounded">Planned</span>
              </div>
              <div className="border border-gray-200 rounded-lg p-4 flex justify-between items-center">
                <div>
                  <div className="font-medium text-gray-900">Context + Linguistic Features</div>
                  <div className="text-sm text-gray-600">Hybrid model with POS, dependency, and discourse markers</div>
                </div>
                <span className="text-xs px-2 py-1 bg-yellow-100 text-yellow-700 rounded">Planned</span>
              </div>
            </div>
          </section>

          {/* Quick Start */}
          <section className="border-t border-gray-200 pt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">Get Started</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Link
                href="/workbench"
                className="block border border-gray-200 rounded-lg p-6 hover:border-indigo-300 hover:shadow-md transition-all"
              >
                <h3 className="font-semibold text-gray-900 mb-2">Analysis Workbench</h3>
                <p className="text-sm text-gray-600">
                  Enter conversations and run pragmatic inference with trained models
                </p>
              </Link>
              <Link
                href="/experiments"
                className="block border border-gray-200 rounded-lg p-6 hover:border-indigo-300 hover:shadow-md transition-all"
              >
                <h3 className="font-semibold text-gray-900 mb-2">Experiments</h3>
                <p className="text-sm text-gray-600">
                  Train models, compare context windows, and view evaluation metrics
                </p>
              </Link>
              <Link
                href="/datasets"
                className="block border border-gray-200 rounded-lg p-6 hover:border-indigo-300 hover:shadow-md transition-all"
              >
                <h3 className="font-semibold text-gray-900 mb-2">Datasets</h3>
                <p className="text-sm text-gray-600">
                  Explore Circa and other pragmatic inference datasets
                </p>
              </Link>
            </div>
          </section>

          {/* Implementation Status */}
          <section className="bg-gray-50 border border-gray-200 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Implementation Status</h2>
            <div className="space-y-2 text-sm">
              <div className="flex items-center">
                <span className="w-3 h-3 bg-green-500 rounded-full mr-3"></span>
                <span className="text-gray-700">Dataset schemas and validation</span>
              </div>
              <div className="flex items-center">
                <span className="w-3 h-3 bg-green-500 rounded-full mr-3"></span>
                <span className="text-gray-700">FastAPI backend with inference endpoints</span>
              </div>
              <div className="flex items-center">
                <span className="w-3 h-3 bg-green-500 rounded-full mr-3"></span>
                <span className="text-gray-700">TF-IDF + Logistic Regression baseline</span>
              </div>
              <div className="flex items-center">
                <span className="w-3 h-3 bg-yellow-500 rounded-full mr-3"></span>
                <span className="text-gray-700">Evidence generation and faithfulness evaluation</span>
              </div>
              <div className="flex items-center">
                <span className="w-3 h-3 bg-yellow-500 rounded-full mr-3"></span>
                <span className="text-gray-700">Transformer models</span>
              </div>
            </div>
          </section>
        </div>
      </main>

      <footer className="border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-sm text-gray-600">
            Computational Linguistics Research Project · MIT License for Code
          </p>
        </div>
      </footer>
    </div>
  );
}
