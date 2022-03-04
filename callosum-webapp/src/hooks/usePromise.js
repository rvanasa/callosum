import {useEffect, useState} from 'react';

export default function usePromise(promise, defaultValue) {
    const [value, setValue] = useState(defaultValue);
    const [error, setError] = useState();
    const [status, setStatus] = useState(null);

    useEffect(() => {
        promise.then(
            // Success
            value => {
                setStatus('resolved');
                setValue(value);
            },
            // Error
            error => {
                setStatus('rejected');
                setError(error);
            },
        );
    });

    return [value, error, status];
}