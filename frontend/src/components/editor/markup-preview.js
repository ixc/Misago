// jshint ignore:start
import React from 'react';
import MisagoMarkup from 'misago/components/misago-markup';

export default function(props) {
  return (
    <div className="modal-dialog" role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button
            aria-label={gettext("Close")}
            className="close"
            data-dismiss="modal"
            type="button"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{gettext("Preview message")}</h4>
        </div>
        <div className="modal-body markup-preview">
          <MisagoMarkup markup={props.markup} />
          {props.post.poster_signature_parsed ?
            <div
              className="signature"
              dangerouslySetInnerHTML={{__html: props.post.poster_signature_parsed}}
            /> : null}
        </div>
      </div>
    </div>
  );
}