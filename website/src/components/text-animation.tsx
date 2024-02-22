import React, { useState, useEffect } from 'react';

// Mapping of regular characters to Braille equivalents
const brailleMap = {
  a: '⠁', b: '⠃', c: '⠉', d: '⠙', e: '⠑',
  f: '⠋', g: '⠛', h: '⠓', i: '⠊', j: '⠚',
  k: '⠅', l: '⠇', m: '⠍', n: '⠝', o: '⠕',
  p: '⠏', q: '⠟', r: '⠗', s: '⠎', t: '⠞',
  u: '⠥', v: '⠧', w: '⠺', x: '⠭', y: '⠽',
  z: '⠵',
  ' ': ' '
};

const WritingText = ({ text }) => {
  const [displayedText, setDisplayedText] = useState(text[0]);

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      // append an 'a' 
      //console.log(slice);
      //console.log(braileSlice);
      const slice = text.slice(0, index);
      console.log(slice + brailleMap[text[index].toLowerCase()]);
      setDisplayedText(slice + brailleMap[text[index].toLowerCase()]);
      index++
      if (index >= text.length) {
        clearInterval(interval);
        setDisplayedText(text);
      }
    }, 200); // Adjust typing speed here
    return () => clearInterval(interval);
  }, [text]);

  return <div className="text-2xl">{displayedText}</div>;
}

export default WritingText;

