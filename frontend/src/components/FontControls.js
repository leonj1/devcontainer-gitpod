import React from 'react';

export const codingFonts = [
  'Courier New',
  'Consolas',
  'Fira Code',
  'Inconsolata',
  'JetBrains Mono',
  'Menlo',
  'Monaco',
  'Source Code Pro',
  'Ubuntu Mono',
];

export const fontSizes = [
  '12px', '14px', '16px', '18px', '20px', '22px', '24px'
];

export function FontControls({ selectedFont, selectedFontSize, onFontChange, onFontSizeChange }) {
  return (
    <div className="mb-3 d-flex align-items-center">
      <div className="me-3">
        <label htmlFor="font-select" className="form-label me-2">Font:</label>
        <select
          id="font-select"
          value={selectedFont}
          onChange={onFontChange}
          className="form-select bg-dark text-light"
        >
          {codingFonts.map((font) => (
            <option key={font} value={font}>{font}</option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="font-size-select" className="form-label me-2">Size:</label>
        <select
          id="font-size-select"
          value={selectedFontSize}
          onChange={onFontSizeChange}
          className="form-select bg-dark text-light"
        >
          {fontSizes.map((size) => (
            <option key={size} value={size}>{size}</option>
          ))}
        </select>
      </div>
    </div>
  );
}
