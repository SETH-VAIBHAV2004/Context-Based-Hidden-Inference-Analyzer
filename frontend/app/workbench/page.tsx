"use client";

import { useState } from "react";
import Link from "next/link";

interface DialogueTurn {
  turn_id: string;
  speaker: string;
  text: string;
}

interface InferenceResult {
  status: string;
  model_id: string;
  model_available: boolean;
  literal_utterance: string | null;
  predicted_label: string | null;
  class_probabilities: Record<string, number> | null;
  context_text: string | null;
  evidence: Array<{
    turn_id: string;
    text: string;
    role: string;
    source: string;
  }>;
  limitations: string[];
}

export default function Workbench() {
  const [turns, setTurns] = useState<DialogueTurn[]>([
    { turn_id: "t0", speaker: "X", text: "Can you help me with this?" },
    { turn_id: "t1", speaker: "Y", text: "I'm pretty busy right now." }
  ]);
  const [targetTurnId, setTargetTurnId] = useState("t1");
  const [contextSituation, setContextSituation] = useState("");
  const [modelId, setModelId] = useState("tfidf_lr");
  const [contextWindow, setContextWindow] = useState("prev_1");
  const [result, setResult] = useState<InferenceResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const addTurn = () => {
    const newId = `t${turns.length}`;
    setTurns([...turns, { turn_id: newId, speaker: "Speaker", text: "" }]);
  };

  const updateTurn = (index: number, field: keyof DialogueTurn, value: string) => {
    const updated = [...turns];
    updated[index] = { ...updated[index], [field]: value };
    setTurns(updated);
  };

  const removeTurn = (index: number) => {
    if (turns.length > 1) {
      setTurns(turns.filter((_, i) => i !== index));
    }
  };

  const runInference = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/api/v1/inference", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          turns,
          target_turn_id: targetTurnId,
          context_situation: contextSituation || null,
          model_id: modelId,
          context_window: {
            name: contextWindow,
            include_situation: contextWindow === "situation_prev_1",
            max_previous_turns: contextWindow === "prev_1" ? 1 : contextWindow === "full" ? null : 0
          }
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || "Inference failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error occurred");
    } finally {
      setLoading(false);
    }
  };

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
              <Link href="/workbench" className="text-indigo-600 font-medium">Workbench</Link>
              <Link href="/experiments" className="text-gray-700 hover:text-gray-900">Experiments</Link>
              <Link href="/datasets" className="text-gray-700 hover:text-gray-900">Datasets</Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Pragmatic Analysis Workbench</h1>
          <p className="text-gray-600">
            Enter a multi-turn conversation and analyze pragmatic inference with trained models
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Panel */}
          <div className="space-y-6">
            <div className="border border-gray-200 rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Conversation</h2>
              
              <div className="space-y-4 mb-4">
                {turns.map((turn, index) => (
                  <div key={turn.turn_id} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <label className="text-sm font-medium text-gray-700">
                        Turn {index} - {turn.turn_id}
                      </label>
                      {turns.length > 1 && (
                        <button
                          onClick={() => removeTurn(index)}
                          className="text-sm text-red-600 hover:text-red-700"
                        >
                          Remove
                        </button>
                      )}
                    </div>
                    <input
                      type="text"
                      value={turn.speaker}
                      onChange={(e) => updateTurn(index, "speaker", e.target.value)}
                      placeholder="Speaker"
                      className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <textarea
                      value={turn.text}
                      onChange={(e) => updateTurn(index, "text", e.target.value)}
                      placeholder="Utterance text"
                      rows={2}
                      className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                ))}
              </div>

              <button
                onClick={addTurn}
                className="w-full px-4 py-2 border border-gray-300 rounded text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Add Turn
              </button>
            </div>

            <div className="border border-gray-200 rounded-lg p-6 space-y-4">
              <h2 className="text-lg font-semibold text-gray-900">Configuration</h2>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Context Situation (optional)
                </label>
                <textarea
                  value={contextSituation}
                  onChange={(e) => setContextSituation(e.target.value)}
                  placeholder="Background context or situation"
                  rows={2}
                  className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Target Turn ID
                </label>
                <select
                  value={targetTurnId}
                  onChange={(e) => setTargetTurnId(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  {turns.map(turn => (
                    <option key={turn.turn_id} value={turn.turn_id}>
                      {turn.turn_id} - {turn.speaker}: {turn.text.substring(0, 30)}...
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Model
                </label>
                <select
                  value={modelId}
                  onChange={(e) => setModelId(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="tfidf_lr">TF-IDF + Logistic Regression</option>
                  <option value="transformer_baseline">Transformer Baseline</option>
                  <option value="context_transformer">Context-Aware Transformer</option>
                  <option value="context_features">Context + Features</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Context Window
                </label>
                <select
                  value={contextWindow}
                  onChange={(e) => setContextWindow(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="target_only">Target Only</option>
                  <option value="prev_1">Previous 1 Turn</option>
                  <option value="situation_prev_1">Situation + Previous 1</option>
                  <option value="full">Full Context</option>
                </select>
              </div>

              <button
                onClick={runInference}
                disabled={loading}
                className="w-full px-4 py-3 bg-indigo-600 text-white rounded font-medium hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {loading ? "Running Inference..." : "Run Pragmatic Inference"}
              </button>
            </div>
          </div>

          {/* Results Panel */}
          <div className="space-y-6">
            {error && (
              <div className="border border-red-200 bg-red-50 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-red-900 mb-1">Error</h3>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            {result && (
              <>
                <div className="border border-gray-200 rounded-lg p-6">
                  <h2 className="text-lg font-semibold text-gray-900 mb-4">Prediction</h2>
                  
                  <div className="space-y-3">
                    <div>
                      <div className="text-xs font-medium text-gray-500 mb-1">LITERAL UTTERANCE</div>
                      <div className="text-sm text-gray-900 bg-gray-50 p-3 rounded border border-gray-200">
                        {result.literal_utterance}
                      </div>
                    </div>

                    {result.model_available && result.predicted_label ? (
                      <>
                        <div>
                          <div className="text-xs font-medium text-gray-500 mb-1">PREDICTED INTERPRETATION</div>
                          <div className="text-lg font-semibold text-indigo-600 p-3 bg-indigo-50 rounded border border-indigo-200">
                            {result.predicted_label}
                          </div>
                        </div>

                        {result.class_probabilities && (
                          <div>
                            <div className="text-xs font-medium text-gray-500 mb-2">CLASS PROBABILITIES</div>
                            <div className="space-y-1">
                              {Object.entries(result.class_probabilities)
                                .sort(([, a], [, b]) => b - a)
                                .map(([label, prob]) => (
                                  <div key={label} className="flex items-center text-sm">
                                    <span className="w-24 text-gray-700">{label}</span>
                                    <div className="flex-1 bg-gray-200 rounded h-6 mr-2">
                                      <div
                                        className="bg-indigo-500 h-6 rounded flex items-center justify-end px-2"
                                        style={{ width: `${prob * 100}%` }}
                                      >
                                        <span className="text-xs text-white font-medium">
                                          {(prob * 100).toFixed(1)}%
                                        </span>
                                      </div>
                                    </div>
                                  </div>
                                ))}
                            </div>
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="bg-yellow-50 border border-yellow-200 rounded p-4">
                        <div className="text-sm font-medium text-yellow-900 mb-1">Model Unavailable</div>
                        <div className="text-sm text-yellow-700">
                          The selected model has not been trained yet.
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {result.context_text && (
                  <div className="border border-gray-200 rounded-lg p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-3">Context Used</h2>
                    <div className="text-sm text-gray-700 bg-gray-50 p-4 rounded border border-gray-200 whitespace-pre-wrap font-mono">
                      {result.context_text}
                    </div>
                  </div>
                )}

                {result.evidence && result.evidence.length > 0 && (
                  <div className="border border-gray-200 rounded-lg p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-3">Evidence</h2>
                    <div className="space-y-3">
                      {result.evidence.map((ev, idx) => (
                        <div key={idx} className="border border-gray-200 rounded p-3 bg-gray-50">
                          <div className="flex justify-between items-start mb-2">
                            <span className="text-xs font-medium text-indigo-600">{ev.role}</span>
                            <span className="text-xs text-gray-500">{ev.source}</span>
                          </div>
                          <div className="text-sm text-gray-900">{ev.text}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {result.limitations && result.limitations.length > 0 && (
                  <div className="border border-yellow-200 bg-yellow-50 rounded-lg p-4">
                    <h3 className="text-sm font-semibold text-yellow-900 mb-2">Limitations</h3>
                    <ul className="space-y-1">
                      {result.limitations.map((limitation, idx) => (
                        <li key={idx} className="text-xs text-yellow-800">• {limitation}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            )}

            {!result && !error && !loading && (
              <div className="border border-gray-200 rounded-lg p-12 text-center">
                <p className="text-gray-500">Configure the conversation and click "Run Pragmatic Inference" to see results</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
