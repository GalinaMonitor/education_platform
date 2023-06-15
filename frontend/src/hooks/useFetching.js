import { useState } from "react";
import { error as errorMessage } from "../messages";

export const useFetching = (callback) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const fetching = async (...args) => {
    try {
      setIsLoading(true);
      await callback(...args);
    } catch (error) {
      errorMessage(error.response?.data?.detail);
      setError(error.response?.data?.detail);
    } finally {
      setIsLoading(false);
    }
  };

  return [fetching, isLoading, error];
};
