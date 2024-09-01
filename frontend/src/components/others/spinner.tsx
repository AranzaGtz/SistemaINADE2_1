import React from "react";

const Spinner: React.FC = () => {
  return (
    <div className="flex items-center">
      <div className="w-7 h-7 border-4 border-solid border-gray-300 border-t-black rounded-full animate-spin"></div>
    </div>
  );
};

export { Spinner };
