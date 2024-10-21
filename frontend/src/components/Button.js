import React from "react";

const Button = ({ onClick, label, className }) => {
  return (
    <button onClick={onClick} className={`px-4 py-2 text-white ${className}`}>
      {label}
    </button>
  );
};

export default Button;
