/* jshint ignore:start */
import React from 'react';
import DiffMessage from 'misago/components/threads-list/list/diff-message'; // jshint ignore:line
import Thread from 'misago/components/threads-list/thread/ready'; // jshint ignore:line

export default function(props) {
  return (
    <div className="threads-list ui-ready">
      <ul className="list-group">
        <DiffMessage
          diffSize={props.diffSize}
          applyDiff={props.applyDiff}
        />
        <li>
          <div className="row">
            <div className="col-md-9"></div>
            <div className="col-md-3 hidden-xs hidden-sm thread-last-action-header">
              <p>Last posted</p>
            </div>
          </div>
        </li>
        {props.threads.map((thread) => {
          return (
            <Thread
              activeCategory={props.activeCategory}
              categories={props.categories}
              list={props.list}
              thread={thread}

              showOptions={props.showOptions}
              isSelected={props.selection.indexOf(thread.id) >= 0}

              isBusy={props.busyThreads.indexOf(thread.id) >= 0}
              key={thread.id}
            />
          );
        })}
      </ul>
    </div>
  );
}