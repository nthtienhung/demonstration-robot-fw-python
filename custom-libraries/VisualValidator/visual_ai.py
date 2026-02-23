"""
Visual Validator - AI Visual Comparison Library
Robot Framework library for visual regression testing using OpenCV and SSIM
"""

import os
import cv2
import numpy as np
from typing import Optional, Tuple, Dict, Any
from robot.api import logger
from skimage.metrics import structural_similarity as ssim
from datetime import datetime


class VisualValidator:
    """
    Visual validation library for comparing screenshots using AI techniques.
    Uses SSIM (Structural Similarity Index) for image comparison.
    """

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize VisualValidator with configuration.

        Args:
            config_path: Path to configuration file
        """
        self.threshold = 0.95
        self.baseline_dir = "custom-libraries/VisualValidator/baseline"
        self.current_dir = "robot-tests/results/screenshots/current"
        self.diff_dir = "robot-tests/results/screenshots/diff"

        # Create directories
        self._ensure_directories()

        logger.info("VisualValidator initialized")

    def _ensure_directories(self) -> None:
        """Ensure required directories exist."""
        for directory in [self.baseline_dir, self.current_dir, self.diff_dir]:
            os.makedirs(directory, exist_ok=True)

    def capture_baseline(self, element_name: str, screenshot_path: Optional[str] = None) -> str:
        """
        Capture and save a baseline image for comparison.

        Args:
            element_name: Name/identifier for the element
            screenshot_path: Optional path to existing screenshot

        Returns:
            Path to saved baseline image
        """
        baseline_path = os.path.join(self.baseline_dir, f"{element_name}_baseline.png")

        if screenshot_path and os.path.exists(screenshot_path):
            # Copy existing screenshot to baseline
            img = cv2.imread(screenshot_path)
            cv2.imwrite(baseline_path, img)
        else:
            logger.warn("No screenshot provided, baseline will be created from future capture")

        logger.info(f"Baseline saved: {baseline_path}")
        return baseline_path

    def capture_current(self, element_name: str, screenshot_path: Optional[str] = None) -> str:
        """
        Capture current state image.

        Args:
            element_name: Name/identifier for the element
            screenshot_path: Optional path to existing screenshot

        Returns:
            Path to saved current image
        """
        current_path = os.path.join(self.current_dir, f"{element_name}_current.png")

        if screenshot_path and os.path.exists(screenshot_path):
            # Copy existing screenshot to current
            img = cv2.imread(screenshot_path)
            cv2.imwrite(current_path, img)
        else:
            logger.warn("No screenshot provided for current capture")

        logger.info(f"Current image saved: {current_path}")
        return current_path

    def compare_images(self, baseline_path: str, current_path: str) -> Dict[str, Any]:
        """
        Compare two images and return similarity metrics.

        Args:
            baseline_path: Path to baseline image
            current_path: Path to current image

        Returns:
            Dictionary with comparison results
        """
        # Load images
        baseline_img = cv2.imread(baseline_path)
        current_img = cv2.imread(current_path)

        if baseline_img is None:
            raise ValueError(f"Cannot load baseline image: {baseline_path}")
        if current_img is None:
            raise ValueError(f"Cannot load current image: {current_path}")

        # Convert to grayscale for SSIM
        baseline_gray = cv2.cvtColor(baseline_img, cv2.COLOR_BGR2GRAY)
        current_gray = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)

        # Calculate SSIM
        similarity, diff = ssim(
            baseline_gray,
            current_gray,
            full=True
        )

        # Convert diff to uint8
        diff = (diff * 255).astype("uint8")

        # Calculate pixel difference percentage
        pixel_diff = np.sum(baseline_img != current_img) / baseline_img.size * 100

        result = {
            'similarity': float(similarity),
            'pixel_difference': float(pixel_diff),
            'passed': similarity >= self.threshold,
            'baseline_path': baseline_path,
            'current_path': current_path,
        }

        logger.info(f"Image comparison: similarity={similarity:.4f}, pixel_diff={pixel_diff:.2f}%")

        return result

    def compare_visual(self, element_name: str,
                      baseline_path: Optional[str] = None,
                      current_path: Optional[str] = None,
                      threshold: Optional[float] = None) -> Dict[str, Any]:
        """
        Compare baseline and current images for an element.

        Args:
            element_name: Name/identifier for the element
            baseline_path: Optional path to baseline image
            current_path: Optional path to current image
            threshold: Optional similarity threshold override

        Returns:
            Dictionary with comparison results
        """
        if threshold is not None:
            self.threshold = threshold

        # Determine paths
        if not baseline_path:
            baseline_path = os.path.join(self.baseline_dir, f"{element_name}_baseline.png")

        if not current_path:
            current_path = os.path.join(self.current_dir, f"{element_name}_current.png")

        # Check if baseline exists
        if not os.path.exists(baseline_path):
            logger.warn(f"Baseline not found for {element_name}, creating from current")
            self.capture_baseline(element_name, current_path)
            return {
                'similarity': 1.0,
                'pixel_difference': 0.0,
                'passed': True,
                'message': 'Baseline created from current image'
            }

        # Perform comparison
        result = self.compare_images(baseline_path, current_path)

        # Add element name and threshold to result
        result['element_name'] = element_name
        result['threshold'] = self.threshold

        return result

    def highlight_differences(self, baseline_path: str, current_path: str,
                             output_path: str, highlight_color: Tuple[int, int, int] = (0, 0, 255)) -> str:
        """
        Highlight differences between two images.

        Args:
            baseline_path: Path to baseline image
            current_path: Path to current image
            output_path: Path for output image
            highlight_color: Color for highlighting (BGR format)

        Returns:
            Path to output image with highlighted differences
        """
        # Load images
        baseline_img = cv2.imread(baseline_path)
        current_img = cv2.imread(current_path)

        # Ensure same size
        if baseline_img.shape != current_img.shape:
            current_img = cv2.resize(current_img, (baseline_img.shape[1], baseline_img.shape[0]))

        # Calculate absolute difference
        diff = cv2.absdiff(baseline_img, current_img)

        # Apply threshold to find significant differences
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

        # Create highlighted image
        highlighted = current_img.copy()
        highlighted[thresh > 0] = highlight_color

        # Blend original with highlighted
        blended = cv2.addWeighted(current_img, 0.7, highlighted, 0.3, 0)

        # Add borders around differences
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 10:  # Filter small differences
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(blended, (x, y), (x + w, y + h), highlight_color, 2)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        cv2.imwrite(output_path, blended)
        logger.info(f"Difference highlight saved: {output_path}")

        return output_path

    def create_comparison_report(self, element_name: str,
                                baseline_path: Optional[str] = None,
                                current_path: Optional[str] = None) -> Dict[str, str]:
        """
        Create a side-by-side comparison image.

        Args:
            element_name: Name/identifier for the element
            baseline_path: Optional path to baseline image
            current_path: Optional path to current image

        Returns:
            Dictionary with paths to comparison images
        """
        if not baseline_path:
            baseline_path = os.path.join(self.baseline_dir, f"{element_name}_baseline.png")
        if not current_path:
            current_path = os.path.join(self.current_dir, f"{element_name}_current.png")

        # Load images
        baseline_img = cv2.imread(baseline_path)
        current_img = cv2.imread(current_path)

        if baseline_img is None or current_img is None:
            raise ValueError("Cannot load images for comparison")

        # Resize to match
        height = max(baseline_img.shape[0], current_img.shape[0])
        baseline_img = cv2.resize(baseline_img, (400, int(height * 400 / baseline_img.shape[1])))
        current_img = cv2.resize(current_img, (400, int(height * 400 / current_img.shape[1])))

        # Create side-by-side comparison
        comparison = np.hstack([baseline_img, current_img])

        # Add labels
        cv2.putText(comparison, "BASELINE", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(comparison, "CURRENT", (baseline_img.shape[1] + 10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Save comparison
        output_path = os.path.join(self.diff_dir, f"{element_name}_comparison.png")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, comparison)

        # Create diff highlight
        diff_path = os.path.join(self.diff_dir, f"{element_name}_diff.png")
        self.highlight_differences(baseline_path, current_path, diff_path)

        logger.info(f"Comparison report created: {output_path}")

        return {
            'comparison': output_path,
            'diff': diff_path
        }

    def calculate_mse(self, image1_path: str, image2_path: str) -> float:
        """
        Calculate Mean Squared Error between two images.

        Args:
            image1_path: Path to first image
            image2_path: Path to second image

        Returns:
            MSE value (lower is more similar)
        """
        img1 = cv2.imread(image1_path)
        img2 = cv2.imread(image2_path)

        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        mse = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
        mse /= float(img1.shape[0] * img1.shape[1])

        logger.info(f"MSE between images: {mse:.2f}")
        return mse

    def get_image_dimensions(self, image_path: str) -> Tuple[int, int]:
        """
        Get image dimensions.

        Args:
            image_path: Path to image

        Returns:
            Tuple of (width, height)
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")
        height, width = img.shape[:2]
        return (width, height)

    def resize_image(self, input_path: str, output_path: str,
                    width: Optional[int] = None, height: Optional[int] = None) -> str:
        """
        Resize an image to specified dimensions.

        Args:
            input_path: Path to input image
            output_path: Path for output image
            width: Target width (maintains aspect ratio if only width specified)
            height: Target height (maintains aspect ratio if only height specified)

        Returns:
            Path to resized image
        """
        img = cv2.imread(input_path)
        if img is None:
            raise ValueError(f"Cannot load image: {input_path}")

        original_height, original_width = img.shape[:2]

        if width and height:
            new_size = (width, height)
        elif width:
            ratio = width / original_width
            new_size = (width, int(original_height * ratio))
        elif height:
            ratio = height / original_height
            new_size = (int(original_width * ratio), height)
        else:
            raise ValueError("Must specify at least width or height")

        resized = cv2.resize(img, new_size)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, resized)

        logger.info(f"Image resized: {input_path} -> {output_path} ({new_size})")
        return output_path


# ==================== Robot Framework Library Functions ====================

def capture_baseline(element_name, screenshot_path=None):
    """Robot Framework keyword: Capture baseline image."""
    return VisualValidator().capture_baseline(element_name, screenshot_path)


def capture_current_screenshot(element_name, screenshot_path=None):
    """Robot Framework keyword: Capture current screenshot."""
    return VisualValidator().capture_current(element_name, screenshot_path)


def compare_visual(element_name, baseline_path=None, current_path=None, threshold=None):
    """Robot Framework keyword: Compare visual images."""
    return VisualValidator().compare_visual(element_name, baseline_path, current_path, threshold)


def highlight_differences(baseline_path, current_path, output_path=None):
    """Robot Framework keyword: Highlight differences."""
    if not output_path:
        output_path = f"robot-tests/results/screenshots/diff/{datetime.now().strftime('%Y%m%d_%H%M%S')}_diff.png"
    return VisualValidator().highlight_differences(baseline_path, current_path, output_path)


def create_comparison_report(element_name, baseline_path=None, current_path=None):
    """Robot Framework keyword: Create comparison report."""
    return VisualValidator().create_comparison_report(element_name, baseline_path, current_path)
