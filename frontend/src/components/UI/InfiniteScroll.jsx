import React, {
  forwardRef,
  ReactNode,
  useEffect,
  useLayoutEffect,
  useImperativeHandle,
  useState,
  useRef,
} from "react";
import useScroll from "../../hooks/useScroll";

const InfiniteScroll = forwardRef(
  (
    {
      children,
      initialReverse = true,
      loadingComponent,

      nextDataFn,
      nextEnd,
      nextLoading,
      previousDataFn,
      previousEnd,
      previousLoading,
    },
    ref
  ) => {
    useImperativeHandle(ref, () => {
      return {
        setReverseCol,
        containerRef,
      };
    });

    const [reverseCol, setReverseCol] = useState(initialReverse);
    const [reverseColValue, setReverseColValue] = useState(null);
    const [scrolledToBottom, scrolledToTop, containerRef] =
      useScroll(reverseCol);
    const [loadNext, setLoadNext] = useState(false);
    const [loadPrevious, setLoadPrevious] = useState(false);

    const container = containerRef.current;

    // This is called next render - next flex-col or flex-col-reverse is set
    useLayoutEffect(() => {
      if (reverseColValue !== null) {
        container?.scrollTo({ top: reverseColValue });
      }
    }, [reverseColValue]);

    // Load next
    useEffect(() => {
      if (!container) return;

      if (scrolledToBottom && !nextLoading && !nextEnd && !previousLoading) {
        if (reverseCol) {
          const scrollTo =
            container.scrollTop +
            container.scrollHeight -
            container.clientHeight;
          setReverseCol(false);
          setReverseColValue(scrollTo);
        }

        nextDataFn();
      }
      setLoadNext(false);
    }, [loadNext, scrolledToBottom, reverseCol]);

    // Load previous
    useEffect(() => {
      if (!container) return;

      if (scrolledToTop && !previousLoading && !previousEnd && !nextLoading) {
        if (!reverseCol) {
          const scrollTo =
            container.scrollTop -
            container.scrollHeight -
            container.clientHeight;
          setReverseCol(true);
          setReverseColValue(scrollTo);
        }
        previousDataFn();
      }
      setLoadPrevious(false);
    }, [loadPrevious, scrolledToTop, reverseCol]);

    return (
      <div
        style={{
          display: "flex",
          flexDirection: reverseCol ? "column-reverse" : "column",
          height: "100%",
          overflowY: "scroll",
        }}
        ref={containerRef}
      >
        <div>
          {previousLoading && loadingComponent}
          {children}
          {nextLoading && loadingComponent}
        </div>
      </div>
    );
  }
);

InfiniteScroll.displayName = "InfiniteScroll";

export default InfiniteScroll;
