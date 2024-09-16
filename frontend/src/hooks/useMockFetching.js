import { useState } from "react";
import { error as errorMessage } from "../messages";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export const useMockFetching = (message) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const fetching = async () => {
    setIsLoading(true);
    await sleep(2000);
    errorMessage(message);
    setIsLoading(false);
  };

  return [fetching, isLoading, error];
};
