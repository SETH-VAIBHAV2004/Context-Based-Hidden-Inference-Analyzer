"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface Model {
  id: string;
  name: string;
  trained: boolean;
  trained_on: string | null;
  metrics_available: boolean;
}

interface MetricsRun {
  model_id: string;
  n_examples: number;
  accuracy: number | null;
  macro_f1: number | null;
  per_class: Record<string, {
    precision: number;
    recall: number;
    f1: number;
    support: number;
  }>;
  confusion_matrix: {
    labels: string[];
    matrix: number[][];
  };
  window: {
    name: string;
    include_situation: boolean;
    max_previous_turns: number | null;
  };
  dataset: string;
  is_synthetic_data: boolean;
}

interface TrainResponse {
  status: string;
  model_id: string;
  dataset_used: string;
  n_train: number;
  n_test: number;
  test_metrics: MetricsRun;
  limitations: string[];
}

export default function Experiments() {
  const [models, setModels] = useState<Model[]>([]);
  const [metrics, setMetrics] = useState<MetricsRun[]>([]);
  const [selectedDataset, setSelectedDataset] = useState("synthetic_pragmatics");
  const [selectedModel, setSelectedModel] = useState("tfidf_lr");
  const [selectedWindow, setSelectedWindow] = useState("prev_1");
  const [training, setTraining] = useState(false);
  const [trainResult, setTrainResult] = useState<TrainResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchModels();
    fetchMetrics();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/models");
      const data = await response.json();
      setModels(data.models);
    } catch (err) {
      console.error("Failed to fetch models:", err);
    }
  };

  const fetchMetrics = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/metrics");
      const data = await response.json();
      setMetrics(data.runs || []);
    } catch (err) {
      console.error("Failed to fetch metrics:", err);
    }
  };

  const trainModel = async () => {
    setTraining(true);
    setError(null);
    setTrainResult(null);

    try {
      const response = await fetch("http://localhost:8000/api/v1/train", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          dataset_id: selectedDataset,
          model_id: selectedModel,
          context_window: {
            name: selectedWindow,
            include_situation: selectedWindow === "situation_prev_1",
            max_previous_turns: selectedWindow === "prev_1" ? 1 : selectedWindow === "full" ? null : 0
          },
          seed: 13,
          test_ratio: 0.2
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || "Training failed");
      }

      const data = await response.json();
      setTrainResult(data);
      await fetchModels();
      await fetchMetrics();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error occurred");
    } finally {
      setTraining(false);
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
              <Link href="/workbench" className="text-gray-700 hover:text-gray-900">Workbench</Link>
              <Link href="/experiments" className="text-indigo-600 font-medium">Experiments</Link>
              <Link href="/datasets" className="text-gray-700 hover:text-gray-900">Datasets</Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Experiments & Model Comparison</h1>
          <p className="text-gray-600">
            Train models, compare context windows, and view evaluation metrics
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Training Panel */}
          <div className="lg:col-span-1">
            <div className="border border-gray-200 rounded-lg p-6 sticky top-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Train Model</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Dataset
                  </label>
                  <select
                    value={selectedDataset}
                    onChange={(e) => setSelectedDataset(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="synthetic_pragmatics">Synthetic Fixture</option>
                    <option value="circa">Circa (if configured)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Model
                  </label>
                  <select
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
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
                    value={selectedWindow}
                    onChange={(e) => setSelectedWindow(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="target_only">Target Only</option>
                    <option value="prev_1">Previous 1 Turn</option>
                    <option value="situation_prev_1">Situation + Previous 1</option>
                    <option value="full">Full Context</option>
                  </select>
                </div>

                <button
                  onClick={trainModel}
                  disabled={training}
                  className="w-full px-4 py-3 bg-indigo-600 text-white rounded font-medium hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  {training ? "Training..." : "Train Model"}
                </button>

                {error && (
                  <div className="bg-red-50 border border-red-200 rounded p-3">
                    <p className="text-sm text-red-700">{error}</p>
                  </div>
                )}

                {trainResult && (
                  <div className="bg-green-50 border border-green-200 rounded p-3">
                    <p className="text-sm font-medium text-green-900 mb-1">Training Complete</p>
                    <p className="text-xs text-green-700">
                      {trainResult.n_train} train, {trainResult.n_test} test examples
                    </p>
                    {trainResult.limitations.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-green-300">
                        <p className="text-xs text-green-800">
                          {trainResult.limitations.join(" ")}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2 space-y-6">
            {/* Model Status */}
            <div className="border border-gray-200 rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Model Status</h2>
              <div className="space-y-2">
                {models.map((model) => (
                  <div key={model.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                    <div className="flex-1">
                      <div className="font-medium text-sm text-gray-900">{model.name}</div>
                      <div className="text-xs text-gray-500">
                        {model.trained ? `Trained on ${model.trained_on}` : "Not trained"}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {model.trained && (
                        <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded">
                          Trained
                        </span>
                      )}
                      {model.metrics_available && (
                        <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">
                          Metrics
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Metrics */}
            {metrics.length > 0 ? (
              metrics.map((metric, idx) => (
                <div key={idx} className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold text-gray-900">
                      {models.find(m => m.id === metric.model_id)?.name || metric.model_id}
                    </h2>
                    {metric.is_synthetic_data && (
                      <span className="text-xs px-2 py-1 bg-yellow-100 text-yellow-700 rounded">
                        Synthetic Data
                      </span>
                    )}
                  </div>

                  <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="text-xs text-gray-500 mb-1">Accuracy</div>
                      <div className="text-2xl font-bold text-gray-900">
                        {metric.accuracy !== null ? (metric.accuracy * 100).toFixed(1) + '%' : 'N/A'}
                      </div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="text-xs text-gray-500 mb-1">Macro F1</div>
                      <div className="text-2xl font-bold text-gray-900">
                        {metric.macro_f1 !== null ? (metric.macro_f1 * 100).toFixed(1) + '%' : 'N/A'}
                      </div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="text-xs text-gray-500 mb-1">Test Examples</div>
                      <div className="text-2xl font-bold text-gray-900">{metric.n_examples}</div>
                    </div>
                  </div>

                  <div className="mb-4">
                    <h3 className="text-sm font-semibold text-gray-900 mb-2">Configuration</h3>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>
                        <span className="text-gray-500">Dataset:</span>
                        <span className="ml-2 text-gray-900">{metric.dataset}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Context:</span>
                        <span className="ml-2 text-gray-900">{metric.window.name}</span>
                      </div>
                    </div>
                  </div>

                  {metric.per_class && Object.keys(metric.per_class).length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-900 mb-3">Per-Class Metrics</h3>
                      <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                          <thead>
                            <tr className="border-b border-gray-200">
                              <th className="text-left py-2 pr-4 font-medium text-gray-700">Label</th>
                              <th className="text-right py-2 px-2 font-medium text-gray-700">Precision</th>
                              <th className="text-right py-2 px-2 font-medium text-gray-700">Recall</th>
                              <th className="text-right py-2 px-2 font-medium text-gray-700">F1</th>
                              <th className="text-right py-2 pl-2 font-medium text-gray-700">Support</th>
                            </tr>
                          </thead>
                          <tbody>
                            {Object.entries(metric.per_class).map(([label, scores]) => (
                              <tr key={label} className="border-b border-gray-100">
                                <td className="py-2 pr-4 text-gray-900">{label}</td>
                                <td className="py-2 px-2 text-right text-gray-700">
                                  {(scores.precision * 100).toFixed(1)}%
                                </td>
                                <td className="py-2 px-2 text-right text-gray-700">
                                  {(scores.recall * 100).toFixed(1)}%
                                </td>
                                <td className="py-2 px-2 text-right text-gray-700">
                                  {(scores.f1 * 100).toFixed(1)}%
                                </td>
                                <td className="py-2 pl-2 text-right text-gray-700">{scores.support}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {metric.confusion_matrix && metric.confusion_matrix.matrix.length > 0 && (
                    <div className="mt-6">
                      <h3 className="text-sm font-semibold text-gray-900 mb-3">Confusion Matrix</h3>
                      <div className="overflow-x-auto">
                        <div className="inline-block min-w-full">
                          <table className="text-xs border-collapse">
                            <thead>
                              <tr>
                                <th className="border border-gray-300 p-2 bg-gray-50"></th>
                                {metric.confusion_matrix.labels.map((label) => (
                                  <th key={label} className="border border-gray-300 p-2 bg-gray-50 font-medium text-gray-700">
                                    {label}
                                  </th>
                                ))}
                              </tr>
                            </thead>
                            <tbody>
                              {metric.confusion_matrix.matrix.map((row, i) => (
                                <tr key={i}>
                                  <td className="border border-gray-300 p-2 bg-gray-50 font-medium text-gray-700">
                                    {metric.confusion_matrix.labels[i]}
                                  </td>
                                  {row.map((cell, j) => (
                                    <td
                                      key={j}
                                      className={`border border-gray-300 p-2 text-center ${
                                        i === j ? 'bg-green-50 font-semibold' : 'bg-white'
                                      }`}
                                    >
                                      {cell}
                                    </td>
                                  ))}
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))
            ) : (
              <div className="border border-gray-200 rounded-lg p-12 text-center">
                <p className="text-gray-500 mb-4">No evaluation metrics available yet</p>
                <p className="text-sm text-gray-400">Train a model to see evaluation results</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
