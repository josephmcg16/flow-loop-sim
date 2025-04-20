import React from "react";

interface Props {
    onClick: () => void;
    disabled?: boolean;
}

export default function RunButton({ onClick, disabled }: Props) {
    return (
        <button onClick={onClick} disabled={disabled}>
            {disabled ? "Running…" : "Run simulation"}
        </button>
    );
}
