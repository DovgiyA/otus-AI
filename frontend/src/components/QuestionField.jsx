import React from 'react';

/**
 * Reusable component for rendering a single survey question.
 * Supports both 'text' input and 'radio' (multiple choice) question types.
 */
export default function QuestionField({ question, value, onChange }) {
  const handleChange = (e) => {
    onChange(question.id, e.target.value);
  };

  return (
    <div className="question-field">
      <label className="question-label">{question.text}</label>

      {question.type === 'text' && (
        <input
          type="text"
          className="question-input"
          value={value}
          onChange={handleChange}
          placeholder="Enter your answer..."
          required
        />
      )}

      {question.type === 'radio' && (
        <fieldset className="question-radio-group">
          {question.options &&
            question.options.map((option) => (
              <div key={option} className="radio-option">
                <input
                  type="radio"
                  id={`q${question.id}_${option}`}
                  name={`question_${question.id}`}
                  value={option}
                  checked={value === option}
                  onChange={handleChange}
                  required
                />
                <label htmlFor={`q${question.id}_${option}`} className="radio-label">
                  {option}
                </label>
              </div>
            ))}
        </fieldset>
      )}
    </div>
  );
}
