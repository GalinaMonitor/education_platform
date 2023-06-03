import { throttle } from "lodash";
import { useEffect, useRef, useState } from "react";

// reverse should be set to true if the DOM element is `flex-col-reverse`
const useScroll = (reverse) => {
  const containerRef = useRef(null);
  const [isBottom, setIsBottom] = useState(false);
  const [isTop, setIsTop] = useState(false);

  const updateScroll = () => {
    const container = containerRef.current;
    if (!container) return;

    if (reverse) {
      if (container.scrollTop === 0) {
        setIsBottom(true);
      } else {
        setIsBottom(false);
      }

      if (
        container.scrollTop - container.clientHeight + container.scrollHeight <=
        20
      ) {
        setIsTop(true);
      } else {
        setIsTop(false);
      }
    } else {
      if (
        container.scrollHeight - container.clientHeight - container.scrollTop <=
        20
      ) {
        setIsBottom(true);
      } else {
        setIsBottom(false);
      }

      if (container.scrollTop === 0) {
        setIsTop(true);
      } else {
        setIsTop(false);
      }
    }
  };

  useEffect(() => {
    updateScroll();

    const handleScroll = throttle(() => {
      updateScroll();
    }, 100);

    if (containerRef.current) {
      containerRef.current.addEventListener("scroll", handleScroll, {
        passive: true,
      });
    }

    return () => {
      if (containerRef.current) {
        containerRef.current.removeEventListener("scroll", handleScroll);
      }
    };
  }, [containerRef.current, reverse]);

  return [isBottom, isTop, containerRef];
};

export default useScroll;
