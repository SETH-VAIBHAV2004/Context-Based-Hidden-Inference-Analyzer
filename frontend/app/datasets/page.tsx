"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface Dataset {
  id: string;
  name: string;
  language: string;
  is_synthetic: boolean;
  n_examples: number | null;
  labels: Record<string, number> | null;
  license: string;
  citation: string;
  source?: string;
  available: boolean;
  limitation?: string;
}

export default function Datasets() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/datasets");
      const data = await response.json();
      setDatasets(data.datasets || []);
    } catch (err) {
      console.error("Failed to fetch datasets:", err);
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
              <Link href="/workbench" className="text-gray-700 hover:text-gray-900">Workbench</Link>
              <Link href="/experiments" className="text-gray-700 hover:text-gray-900">Experiments</Link>
              <Link href="/datasets" className="text-indigo-600 font-medium">Datasets</Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dataset Explorer</h1>
          <p className="text-gray-600">
            Explore pragmatic inference datasets with license and attribution information
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-500">Loading datasets...</p>
          </div>
        ) : (
          <div className="space-y-6">
            {datasets.map((dataset) => (
              <div key={dataset.id} className="border border-gray-200 rounded-lg p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900 mb-1">
                      {dataset.name}
                    </h2>
                    <div className="flex items-center space-x-3 text-sm">
                      <span className="text-gray-600">Language: {dataset.language}</span>
                      {dataset.is_synthetic && (
                        <span className="px-2 py-0.5 bg-yellow-100 text-yellow-700 rounded text-xs font-medium">
                          Synthetic
                        </span>
                      )}
                      {dataset.available ? (
                        <span className="px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs font-medium">
                          Available
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 bg-gray-100 text-gray-700 rounded text-xs font-medium">
                          Not Configured
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {dataset.n_examples !== null && (
                  <div className="mb-4">
                    <div className="text-sm font-medium text-gray-700 mb-2">Statistics</div>
                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="text-sm text-gray-900 mb-3">
                        <span className="font-semibold">{dataset.n_examples}</span> examples
                      </div>
                      
                      {dataset.labels && Object.keys(dataset.labels).length > 0 && (
                        <div>
                          <div className="text-xs font-medium text-gray-600 mb-2">Label Distribution</div>
                          <div className="space-y-1.5">
                            {Object.entries(dataset.labels)
                              .sort(([, a], [, b]) => b - a)
                              .map(([label, count]) => {
                                const percentage = dataset.n_examples 
                                  ? ((count / dataset.n_examples) * 100).toFixed(1)
                                  : "0";
                                return (
                                  <div key={label} className="flex items-center">
                                    <span className="text-xs text-gray-700 w-32">{label}</span>
                                    <div className="flex-1 bg-gray-200 rounded h-5 mr-2">
                                      <div
                                        className="bg-indigo-500 h-5 rounded flex items-center justify-end px-2"
                                        style={{ width: `${percentage}%` }}
                                      >
                                        {parseFloat(percentage) > 15 && (
                                          <span className="text-xs text-white font-medium">
                                            {count}
                                          </span>
                                        )}
                                      </div>
                                    </div>
                                    {parseFloat(percentage) <= 15 && (
                                      <span className="text-xs text-gray-600 w-12 text-right">
                                        {count}
                                      </span>
                                    )}
                                  </div>
                                );
                              })}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                <div className="mb-4">
                  <div className="text-sm font-medium text-gray-700 mb-2">License</div>
                  <p className="text-sm text-gray-600 bg-gray-50 rounded p-3 border border-gray-200">
                    {dataset.license}
                  </p>
                </div>

                <div className="mb-4">
                  <div className="text-sm font-medium text-gray-700 mb-2">Citation</div>
                  <p className="text-sm text-gray-600 bg-gray-50 rounded p-3 border border-gray-200 font-mono">
                    {dataset.citation}
                  </p>
                </div>

                {dataset.source && (
                  <div className="mb-4">
                    <div className="text-sm font-medium text-gray-700 mb-2">Source</div>
                    <a
                      href={dataset.source}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-indigo-600 hover:text-indigo-700 underline"
                    >
                      {dataset.source}
                    </a>
                  </div>
                )}

                {dataset.limitation && (
                  <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
                    <div className="text-xs font-medium text-yellow-900 mb-1">Note</div>
                    <p className="text-xs text-yellow-700">{dataset.limitation}</p>
                  </div>
                )}
              </div>
            ))}

            {/* Dataset Information */}
            <div className="border-t border-gray-200 pt-8 mt-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">About Circa</h2>
              <div className="prose prose-sm max-w-none text-gray-700 space-y-3">
                <p>
                  Circa (Conversational Inference from Responses and Context in an Argument) is a dataset 
                  for pragmatic inference in indirect answers to polar questions. It was introduced by 
                  Louis, Roth, and Radlinski at EMNLP 2020.
                </p>
                <p>
                  The dataset contains question-answer pairs with contextual situations. Each example 
                  includes a situation description, a polar question from speaker X, an answer from speaker Y, 
                  and a gold interpretation label indicating what Y's answer means pragmatically 
                  (yes, no, conditional, middle, or other).
                </p>
                <p className="text-sm text-gray-600">
                  <strong>To use Circa:</strong> Download the official TSV file from the{" "}
                  <a 
                    href="https://github.com/google-research-datasets/circa" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-indigo-600 hover:text-indigo-700 underline"
                  >
                    GitHub repository
                  </a>
                  {" "}and set the <code className="bg-gray-100 px-1 py-0.5 rounded">CIRCA_PATH</code> environment 
                  variable to point to the file location.
                </p>
              </div>
            </div>

            <div className="border-t border-gray-200 pt-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Data Validation</h2>
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 space-y-3 text-sm text-gray-700">
                <div className="flex items-start">
                  <div className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div>
                    <strong>Schema Validation:</strong> All loaded examples are validated against Pydantic schemas
                  </div>
                </div>
                <div className="flex items-start">
                  <div className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div>
                    <strong>Group-Aware Splits:</strong> Examples sharing a question are kept in the same split to prevent data leakage
                  </div>
                </div>
                <div className="flex items-start">
                  <div className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div>
                    <strong>Label Normalization:</strong> Circa labels are mapped to consistent categories and NA values are excluded
                  </div>
                </div>
                <div className="flex items-start">
                  <div className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div>
                    <strong>Duplicate Detection:</strong> Automated checks identify potential duplicate examples
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
