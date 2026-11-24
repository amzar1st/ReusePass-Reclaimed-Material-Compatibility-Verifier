export function classifyTransaction(tx) {
  if (!tx) return { state: "UNKNOWN", label: "Not found yet", terminal: false };
  const status = String(tx.status ?? "UNKNOWN").toUpperCase();
  const execution = String(
    tx.execution_result ??
      tx.txExecutionResultName ??
      tx.consensus_data?.leader_receipt?.execution_result ??
      "",
  ).toUpperCase();
  if (["CANCELED", "CANCELLED", "UNDETERMINED"].includes(status))
    return { state: "FAILED", label: status, terminal: true };
  if (
    [
      "ERROR",
      "REVERT",
      "REVERTED",
      "CONTRACT_ERROR",
      "VM_ERROR",
      "DISAGREE",
      "FINISHED_WITH_ERROR",
      "FINISHED_WITH_REVERT",
      "FINISHED_WITH_VM_ERROR",
      "FINISHED_WITH_USER_ERROR",
    ].includes(execution)
  )
    return { state: "FAILED", label: `Execution ${execution}`, terminal: true };
  if (status === "FINALIZED") {
    if (!["SUCCESS", "RETURN", "FINISHED_WITH_RETURN"].includes(execution))
      return {
        state: "UNVERIFIED",
        label: "Finalized · verify execution",
        terminal: true,
      };
    return {
      state: "SUCCESS",
      label: "Finalized · execution succeeded",
      terminal: true,
    };
  }
  return {
    state: "PENDING",
    label: status === "ACCEPTED" ? "Accepted · awaiting finality" : status,
    terminal: false,
  };
}
export function validateHash(hash) {
  return /^0x[0-9a-fA-F]{64}$/.test(hash);
}
export function safeParse(value, fallback) {
  try {
    return JSON.parse(value);
  } catch {
    return fallback;
  }
}
