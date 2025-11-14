from pydantic import BaseModel, Field
from typing import List

# =========Topic Generation Schema=========
class BasicTopicScore(BaseModel):
    """Basic scoring structure for AI generation"""
    relevance: float = Field(..., ge=0, le=1, description="How relevant to the industry/domain")
    seo_potential: float = Field(..., ge=0, le=1, description="SEO ranking potential")
    trend_level: float = Field(..., ge=0, le=1, description="How trending/popular this topic is")
    uniqueness: float = Field(..., ge=0, le=1, description="How original compared to existing content")
    reader_interest: float = Field(..., ge=0, le=1, description="Engagement potential with readers")
    actionable_potential: float = Field(..., ge=0, le=1, description="How suitable for how-to/tutorial content")
    brand_alignment: float = Field(..., ge=0, le=1, description="How well it fits brand voice")
    controversy: float = Field(..., ge=0, le=1, description="Potential for debate/polarization (lower = safer)")


    # suggested_defaults = Column(JSONB, nullable=False)  # New fieldm
    # goal_alignment = Column(JSONB, nullable=False)  # New field ...
    # content_guidance = Column(JSONB, nullable=False)  # New field
    # audience_insights = Column(JSONB, nullable=False)  # New field
    # internal_research_config = Column(JSONB, nullable=False)  # New field
    # approved = Column(Boolean, nullable=True, server_default="false")
    # approved_at = Column(DateTime(timezone=True), nullable=True)  # When topic was approved
    # user_settings = Column(JSONB, nullable=False)  # New field


class BasicTopicGeneration(BaseModel):
    """Basic topic structure for AI generation before enrichment"""
    title: str = Field(..., description="Main headline for the content")
    angle: str = Field(..., description="Unique perspective or approach")
    description: str = Field(..., description="Detailed explanation of what the content will cover")
    channel_fit: List[str] = Field(..., description="Best platforms for this content")
    audience_fit: List[str] = Field(..., description="Target audience segments")
    why_it_works: str = Field(..., description="Justification for why this topic is valuable")
    tags: List[str] = Field(..., description="Categorization tags")
    scores: BasicTopicScore = Field(..., description="Basic scoring from AI generation")

class BasicTopicGenerationList(BaseModel):
    topics: List[BasicTopicGeneration]
