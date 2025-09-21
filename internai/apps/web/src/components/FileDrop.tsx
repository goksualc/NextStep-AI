import React, { useState, useRef, DragEvent } from 'react';

interface FileDropProps {
  onFileSelect: (file: File) => void;
  accept?: string;
  maxSize?: number; // in MB
  className?: string;
}

export const FileDrop: React.FC<FileDropProps> = ({
  onFileSelect,
  accept = '.pdf',
  maxSize = 10,
  className = ''
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): boolean => {
    // Check file size
    if (file.size > maxSize * 1024 * 1024) {
      setError(`File size must be less than ${maxSize}MB`);
      return false;
    }

    // Check file type
    if (accept && !file.name.toLowerCase().match(accept.replace('*', '.*'))) {
      setError(`File type must be ${accept}`);
      return false;
    }

    setError(null);
    return true;
  };

  const handleFile = (file: File) => {
    if (validateFile(file)) {
      onFileSelect(file);
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0 && files[0]) {
      handleFile(files[0]);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0 && files[0]) {
      handleFile(files[0]);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const baseClasses = 'border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-colors duration-200';
  const stateClasses = isDragOver 
    ? 'border-primary-400 bg-primary-50' 
    : error 
      ? 'border-red-300 bg-red-50' 
      : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50';

  return (
    <div className={className}>
      <div
        className={`${baseClasses} ${stateClasses}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <div className="flex flex-col items-center space-y-4">
          <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center">
            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          
          <div>
            <p className="text-lg font-medium text-gray-900">
              Drop your resume here
            </p>
            <p className="text-sm text-gray-500 mt-1">
              or click to browse files
            </p>
            <p className="text-xs text-gray-400 mt-2">
              PDF files up to {maxSize}MB
            </p>
          </div>
        </div>
      </div>
      
      {error && (
        <p className="mt-3 text-sm text-red-600 text-center">{error}</p>
      )}
      
      <input
        ref={fileInputRef}
        type="file"
        accept={accept}
        onChange={handleFileInputChange}
        className="hidden"
      />
    </div>
  );
};
