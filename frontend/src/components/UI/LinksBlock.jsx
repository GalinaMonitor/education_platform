import React from "react";
import { Link } from "react-router-dom";
import { RouteNames } from "../../router";

const LinksBlock = ({ className }) => {
  return (
    <div className={`${className} flex flex-col justify-around items-end`}>
      <Link to={RouteNames.PRIVACY}>ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ</Link>
      <Link className={"my-1"} to={RouteNames.PRIVACY}>
        ПУБЛИЧНАЯ ОФЕРТА
      </Link>
      <Link to={RouteNames.PRIVACY}>ОПЛАТА И ВОЗВРАТ</Link>
    </div>
  );
};

export default LinksBlock;
