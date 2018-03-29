// jshint ignore:start
import React from 'react';


export default function({ category }) {
  if (! (
      category.acl.can_browse &&
      category.acl.can_see_all_threads &&
      category.last_thread_title
    )
  ) {
    return (<div className="col-md-3 hidden-xs hidden-sm category-last-thread-date">&nbsp;</div>);
  }

  return (
    <div className="col-md-3 hidden-xs hidden-sm category-last-thread-date">
      <a href={category.url.last_post}>Latest post {category.last_post_on.fromNow()}</a>
    </div>
  );
}
