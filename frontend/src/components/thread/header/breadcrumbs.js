/* jshint ignore:start */
import React from 'react';

export default function(props) {
  // example: HOME / CONTEMPORARY TIMEPIECES / Most collectible modern timepieces
  return (
    <div className="page-breadcrumbs">
      <div className="container">
        <ol className="breadcrumb hidden-xs">
          <li><a href="/">Home</a></li>
          <li><a href={props.thread.category.url.index}>{props.thread.category.name}</a></li>
          <li><a href="#">{props.thread.title}</a></li>
        </ol>
      </div>
    </div>
  );
}

//export function Breadcrumb(props) {
//  return (
//    <li>
//      <a href={props.node.url.index}>{props.node.name}</a>
//    </li>
//  );
//}
//
//export function GoBack(props) {
//  const lastItem = props.path[props.path.length - 1];
//
//  return (
//    <a href={lastItem.url.index} className="go-back-sm visible-xs-block">
//      <span className="material-icon">
//        chevron_left
//      </span>
//      {lastItem.name}
//    </a>
//  );
//}
/* jshint ignore:end */