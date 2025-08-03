// src/components/quizzes/CodeEditor.js
import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import './CodeEditor.css';

/**
 * Code Editor component for coding questions
 * @param {object} props - Component props
 * @param {string} props.language - Programming language
 * @param {string} props.defaultCode - Default code template
 * @param {function} props.onCodeChange - Callback when code changes
 * @param {string} props.value - Current code value
 * @param {boolean} props.readOnly - Whether editor is read-only
 * @param {object} props.theme - Editor theme (light/dark)
 */
const CodeEditor = ({ 
  language = 'javascript', 
  defaultCode = '', 
  onCodeChange, 
  value = '', 
  readOnly = false,
  theme = 'light'
}) => {
  const [code, setCode] = useState(value || defaultCode);

  const handleEditorChange = (value) => {
    setCode(value);
    onCodeChange && onCodeChange(value);
  };

  const editorOptions = {
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    fontSize: 14,
    lineNumbers: 'on',
    roundedSelection: false,
    readOnly: readOnly,
    cursorStyle: 'line',
    automaticLayout: true,
    scrollbar: {
      vertical: 'visible',
      horizontal: 'visible',
      verticalScrollbarSize: 10,
      horizontalScrollbarSize: 10,
    },
    folding: true,
    wordWrap: 'on',
    suggestOnTriggerCharacters: true,
    quickSuggestions: true,
    parameterHints: {
      enabled: true,
    },
    hover: {
      enabled: true,
    },
    contextmenu: true,
    mouseWheelZoom: true,
    smoothScrolling: true,
    tabSize: 2,
    insertSpaces: true,
    detectIndentation: true,
    trimAutoWhitespace: true,
    largeFileOptimizations: true,
  };

  return (
    <div className="code-editor-container">
      <div className="code-editor-header">
        <span className="language-badge">{language}</span>
        {readOnly && <span className="readonly-badge">Read Only</span>}
      </div>
      <Editor
        height="400px"
        defaultLanguage={language}
        defaultValue={defaultCode}
        value={code}
        onChange={handleEditorChange}
        theme={theme === 'dark' ? 'vs-dark' : 'vs'}
        options={editorOptions}
        className="monaco-editor-container"
      />
    </div>
  );
};

export default CodeEditor; 