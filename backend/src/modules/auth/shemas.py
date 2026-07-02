
"""

class UserModel(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(
        String, 
        CheckConstraint("login ~ '^[a-zA-Z0-9]+$'"), 
        unique=True, 
        nullable=False, 
        index=True
    )
    password_hash: Mapped[str] = mapped_column(
        Text, 
        CheckConstraint("password_hash !~ '\\s'"),
        nullable=False, 
        index=True
    )
"""        