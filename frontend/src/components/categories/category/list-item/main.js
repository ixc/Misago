// jshint ignore:start
import React from 'react';
import Description from './description';
import Icon from './icon';

export default function({ category }) {
  return (
    <div className="col-md-8 category-main">
      <div className="media">
        <div className="media-body">
          <h4 className="media-heading">
            <a href={category.url.index}>
              {category.name}
            </a>
          </h4>
          <Description category={category} />
        </div>
      </div>
    </div>
  );
}